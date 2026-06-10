package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

const MaxRetries = 3

type Payload struct {
	MessageID  string `json:"messageId"`
	RetryCount int    `json:"retryCount"`

	Temperature         float64 `json:"temperature"`
	Windspeed           float64 `json:"windspeed"`
	Humidity            float64 `json:"humidity"`
	UVIndex             float64 `json:"uvIndex"`
	PrecipitationChance float64 `json:"precipitationChance"`
	HeatIndex           float64 `json:"heatIndex"`
	Timestamp           string  `json:"timestamp"`
	ObsTimestamp        string  `json:"obs_timestamp"`
	Source              string  `json:"source"`
	Condition           string  `json:"condition"`
}

func getEnv(key string) string {
	val := os.Getenv(key)

	if val == "" {
		log.Fatalf(
			"Variável de ambiente obrigatória não definida: %s",
			key,
		)
	}

	return val
}

func main() {
	for {
		err := runWorker()

		log.Println(
			"Worker error, retrying in 5s:",
			err,
		)

		time.Sleep(5 * time.Second)
	}
}

func publishToDLQ(
	ch *amqp.Channel,
	dlqName string,
	payload Payload,
) {

	body, _ := json.Marshal(payload)

	err := ch.Publish(
		"",
		dlqName,
		false,
		false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		},
	)

	if err != nil {
		log.Println(
			"Erro ao enviar para DLQ:",
			err,
		)
		return
	}

	log.Printf(
		"Mensagem %s enviada para DLQ\n",
		payload.MessageID,
	)
}

func republishMessage(
	ch *amqp.Channel,
	queueName string,
	payload Payload,
) error {

	payload.RetryCount++

	body, err := json.Marshal(payload)

	if err != nil {
		return err
	}

	return ch.Publish(
		"",
		queueName,
		false,
		false,
		amqp.Publishing{
			ContentType:  "application/json",
			DeliveryMode: 2,
			Body:         body,
		},
	)
}

func runWorker() error {

	rabbitURL := getEnv("RABBITMQ_URL")
	queueName := getEnv("RABBITMQ_QUEUE")
	backendURL := getEnv("BACKEND_INTERNAL_URL")
	workerSecret := getEnv("WORKER_SECRET")

	dlqName := queueName + ".dlq"

	conn, err := amqp.Dial(rabbitURL)

	if err != nil {
		return fmt.Errorf(
			"rabbitmq dial: %v",
			err,
		)
	}

	defer conn.Close()

	ch, err := conn.Channel()

	if err != nil {
		return fmt.Errorf(
			"channel: %v",
			err,
		)
	}

	defer ch.Close()

	_, err = ch.QueueDeclare(
		dlqName,
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		return fmt.Errorf(
			"dlq declare: %v",
			err,
		)
	}

	q, err := ch.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		return fmt.Errorf(
			"queue declare: %v",
			err,
		)
	}

	msgs, err := ch.Consume(
		q.Name,
		"",
		false,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		return fmt.Errorf(
			"consume: %v",
			err,
		)
	}

	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	log.Println(
		"Worker iniciado e aguardando mensagens...",
	)

	for d := range msgs {

		var p Payload

		if err := json.Unmarshal(
			d.Body,
			&p,
		); err != nil {

			log.Println(
				"Payload inválido:",
				err,
			)

			d.Ack(false)
			continue
		}

		body, _ := json.Marshal(p)

		req, err := http.NewRequest(
			"POST",
			backendURL,
			bytes.NewReader(body),
		)

		if err != nil {

			log.Println(
				"Erro ao criar request:",
				err,
			)

			d.Nack(false, true)
			continue
		}

		req.Header.Set(
			"Content-Type",
			"application/json",
		)

		req.Header.Set(
			"X-WORKER-SECRET",
			workerSecret,
		)

		resp, err := client.Do(req)

		if err != nil {

			log.Printf(
				"Falha msg=%s retry=%d\n",
				p.MessageID,
				p.RetryCount,
			)

			if p.RetryCount >= MaxRetries {

				publishToDLQ(
					ch,
					dlqName,
					p,
				)

			} else {

				republishMessage(
					ch,
					queueName,
					p,
				)
			}

			d.Ack(false)

			continue
		}

		resp.Body.Close()

		if resp.StatusCode >= 400 {

			log.Printf(
				"Backend erro msg=%s retry=%d status=%d\n",
				p.MessageID,
				p.RetryCount,
				resp.StatusCode,
			)

			if p.RetryCount >= MaxRetries {

				publishToDLQ(
					ch,
					dlqName,
					p,
				)

			} else {

				republishMessage(
					ch,
					queueName,
					p,
				)
			}

			d.Ack(false)

			continue
		}

		d.Ack(false)

		log.Printf(
			"Processado msg=%s\n",
			p.MessageID,
		)
	}

	return fmt.Errorf("channel closed")
}
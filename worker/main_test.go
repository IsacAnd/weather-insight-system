package main

import (
	"encoding/json"
	"testing"
)

func TestPayloadJSONParsing(t *testing.T) {
	// JSON válido que representa o payload enviado pelo Producer
	jsonData := `{
		"messageId": "msg-12345",
		"retryCount": 2,
		"temperature": 28.5,
		"windspeed": 10.2,
		"humidity": 75.0,
		"uvIndex": 6.0,
		"precipitationChance": 15.0,
		"heatIndex": 30.1,
		"timestamp": "2026-06-12T18:30:00Z",
		"obs_timestamp": "2026-06-12T18:00:00Z",
		"source": "weather-api",
		"condition": "Ensolarado"
	}`

	var p Payload
	err := json.Unmarshal([]byte(jsonData), &p)
	if err != nil {
		t.Fatalf("Erro inesperado ao fazer unmarshal do JSON: %v", err)
	}

	// Validando se os campos foram populados corretamente
	if p.MessageID != "msg-12345" {
		t.Errorf("Esperado MessageID 'msg-12345', obtido '%s'", p.MessageID)
	}
	if p.RetryCount != 2 {
		t.Errorf("Esperado RetryCount 2, obtido %d", p.RetryCount)
	}
	if p.Temperature != 28.5 {
		t.Errorf("Esperado Temperature 28.5, obtido %f", p.Temperature)
	}
	if p.Condition != "Ensolarado" {
		t.Errorf("Esperado Condition 'Ensolarado', obtido '%s'", p.Condition)
	}
	if p.Source != "weather-api" {
		t.Errorf("Esperado Source 'weather-api', obtido '%s'", p.Source)
	}
}

func TestPayloadJSONParsing_InvalidJSON(t *testing.T) {
	invalidJSON := `{
		"messageId": "msg-123",
		"retryCount": "not-an-int"
	}`

	var p Payload
	err := json.Unmarshal([]byte(invalidJSON), &p)
	if err == nil {
		t.Fatal("Esperado erro ao desserializar JSON com tipo incompatível, mas o erro foi nulo")
	}
}

func TestRetryLimitLogic(t *testing.T) {
	payload := Payload{
		MessageID:  "msg-999",
		RetryCount: 0,
	}

	// Simular o comportamento do worker que incrementa retentativas
	payload.RetryCount++

	if payload.RetryCount != 1 {
		t.Errorf("Esperado RetryCount incrementado para 1, obtido %d", payload.RetryCount)
	}

	// Verifica se a comparação com MaxRetries funciona
	isOverLimit := payload.RetryCount >= MaxRetries
	if isOverLimit {
		t.Errorf("Esperado que a retentativa 1 não ultrapassasse o MaxRetries (%d)", MaxRetries)
	}

	// Atinge o limite
	payload.RetryCount = MaxRetries
	isOverLimit = payload.RetryCount >= MaxRetries
	if !isOverLimit {
		t.Errorf("Esperado que a retentativa %d atingisse ou superasse o limite de MaxRetries (%d)", payload.RetryCount, MaxRetries)
	}
}

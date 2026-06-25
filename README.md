# 🌦️ Weather Insight System — Full Stack com IA, Mensageria e Microsserviços

Sistema completo para coleta, processamento, armazenamento, visualização e geração de **insights inteligentes climáticos**, utilizando:

* **Frontend:** React + Vite
* **Backend:** NestJS
* **Banco de Dados:** MongoDB
* **Mensageria:** RabbitMQ
* **Workers:** Go + Python
* **IA:** DeepSeek via OpenRouter
* **Infraestrutura:** Docker & Docker Compose

---

## 🎯 Objetivo

O **Weather Insight System** foi desenvolvido para demonstrar a utilização de uma arquitetura baseada em microsserviços para coleta, processamento, armazenamento e análise inteligente de dados climáticos em tempo real.

O sistema integra mensageria, banco de dados NoSQL, inteligência artificial e visualização de dados para fornecer insights automáticos sobre condições meteorológicas.

---

## 📸 Demonstração

### Dashboard Principal

<img width="1856" height="860" alt="image" src="https://github.com/user-attachments/assets/7642547d-5182-4fdb-8e3c-c93539ebe959" />

### Gráficos Climáticos

<img width="1180" height="755" alt="image" src="https://github.com/user-attachments/assets/76d7703e-65ac-4dfa-b108-196cd1238956" />

### Insights Gerados por IA

<img width="706" height="366" alt="image" src="https://github.com/user-attachments/assets/46329556-3a5e-4670-9c16-68eddbe74910" />

---

## 📖 Documentação

A documentação completa do projeto está disponível no link abaixo:

📄 **Documentação Oficial:**
https://docs.google.com/document/d/1OzQcOrtPNNc1TJJ3_gxTbEBWRFsNNbMDpYmBoky2Z5o/edit?usp=drivesdk

---

## 🧠 Visão Geral da Arquitetura

```text
[ Open-Meteo API ]
         │
         ▼
[ Producer (Python) ]
         │
         ▼
     [ RabbitMQ ]
         │
         ▼
    [ Worker (Go) ]
         │
         ▼
 [ Backend (NestJS) ]
         │
    ┌────┴────┐
    ▼         ▼
MongoDB   DeepSeek IA
    │
    ▼
Frontend React
```

---

## 🚀 Tecnologias Utilizadas

### Frontend

* React
* Vite
* TypeScript
* TailwindCSS
* React Router
* React Query

### Backend

* NestJS
* TypeScript
* JWT
* Bcrypt
* Mongoose

### Banco de Dados

* MongoDB

### Mensageria

* RabbitMQ

### Inteligência Artificial

* DeepSeek
* OpenRouter

### Infraestrutura

* Docker
* Docker Compose

### Workers

* Python
* Go

---

## ✅ Pré-requisitos

Antes de começar, você precisa ter instalado:

* Docker
* Docker Compose
* Git
* Node.js 20+ (apenas para execução local sem Docker)

---

## 📁 Estrutura do Projeto

```text
weather-insight-system/
│
├── backend/
│   ├── src/
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   └── Dockerfile
│
├── producer/
│   ├── main.py
│   └── Dockerfile
│
├── worker/
│   ├── main.go
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔐 Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
copy .env.example .env
```

Configure sua chave da OpenRouter:

```env
DS_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
```

### Como obter a chave da OpenRouter

1. Acesse: https://openrouter.ai
2. Crie uma conta.
3. Acesse **API Keys**.
4. Gere uma nova chave.
5. Cole a chave no arquivo `.env`.

---

## ⚡ Execução Rápida

### 1. Clonar o projeto

```bash
git clone https://github.com/SEU-USUARIO/weather-insight-system.git

cd weather-insight-system
```

### 2. Criar o arquivo `.env`

```bash
copy .env.example .env
```

### 3. Configurar a chave da IA

```env
DS_API_KEY=sk-or-v1-SUA_CHAVE
```

### 4. Subir todos os containers

```bash
docker compose up --build -d
```

### 5. Verificar containers

```bash
docker ps
```

Todos os serviços devem estar em execução.

---

## 🌐 Serviços Disponíveis

| Serviço     | URL                                                                  |
| ----------- | -------------------------------------------------------------------- |
| Frontend    | [wis-frontend](https://weather-insight-system.vercel.app/dashboard)  |
| Backend API | [wis-backend](https://weather-insight-system.onrender.com)           |
| Worker      | [wis-worker](https://go-worker-zwek.onrender.com)                    | 
| Producer    | [wis-producer](https://go-worker-zwek.onrender.com)                  |

---

## 🧪 Como Testar o Sistema

### 1. Registrar Usuário

Acesse:

```text
http://localhost:8080
```

Clique em:

```text
Register
```

Crie uma conta.

---

### 2. Fazer Login

Utilize as credenciais cadastradas.

---

### 3. Verificar Dashboard

A tela principal deve exibir:

* ✅ Dados climáticos atuais
* ✅ Gráficos climáticos
* ✅ Histórico de registros
* ✅ Insights gerados por IA

---

### 4. Verificar RabbitMQ

Acesse:

```text
http://localhost:15672
```

Credenciais padrão:

```text
Usuário: guest
Senha: guest
```

---

### 5. Verificar MongoDB

Os registros devem ser armazenados automaticamente conforme o Producer coleta novos dados.

---

## 📊 Fluxo de Funcionamento

1. O Producer (Python) coleta dados climáticos da Open-Meteo.
2. Os dados são enviados para o RabbitMQ.
3. O Worker (Go) consome as mensagens.
4. O Worker envia os dados para o Backend.
5. O Backend salva os registros no MongoDB.
6. O Backend envia os dados para a IA (DeepSeek).
7. A IA gera insights automáticos.
8. O Frontend exibe os dados e os insights em tempo real.

---

## ✨ Funcionalidades Implementadas

### RF001 — Cache de Requisições

* Implementado utilizando React Query.
* Cache configurável através do `staleTime`.
* Redução de chamadas redundantes ao backend.
* Reutilização automática de dados previamente carregados.

### RF002 — Dashboard

* Dados climáticos em tempo real.
* Atualização manual dos registros.
* Visualização consolidada das informações.

### RF003 — Gráficos

* Temperatura.
* Umidade.
* Velocidade do vento.
* Índice UV.

### RF004 — Histórico de Registros

* Consulta paginada dos dados armazenados.

### RF005 — Exportação

* Exportação em CSV.
* Exportação em XLSX.

### RF006 — Insights com IA

* Geração automática de insights climáticos.
* Integração com DeepSeek via OpenRouter.

### RF007 — Autenticação

* Cadastro de usuários.
* Login com JWT.
* Rotas protegidas.

---

## ✅ Critérios de Validação

Após iniciar o sistema, verifique:

* Cadastro e login funcionando.
* Dashboard carregando dados climáticos.
* Gráficos sendo exibidos corretamente.
* Insights gerados pela IA.
* RabbitMQ recebendo mensagens.
* MongoDB armazenando registros.
* Exportação CSV e XLSX funcionando.

---

## 🛑 Problemas Comuns

### Containers não iniciam

```bash
docker compose down -v
docker compose up --build -d
```

### IA não gera insights

Verifique se existe no `.env`:

```env
DS_API_KEY=sk-or-v1-...
```

### Frontend não conecta ao backend

Verifique:

```env
VITE_BACKEND_URL=http://localhost:3000
```

### Erro de autenticação no MongoDB

```bash
docker compose down -v
docker compose up --build -d
```

### Erro `data and salt arguments required`

Verifique:

```env
DEFAULT_ADMIN_EMAIL=admin@example.com
DEFAULT_ADMIN_PASSWORD=123456
```

---

## 📚 Conceitos Aplicados

Durante o desenvolvimento deste projeto foram utilizados conceitos de:

* Arquitetura de Microsserviços
* Sistemas Distribuídos
* Mensageria com RabbitMQ
* Processamento Assíncrono
* APIs REST
* Autenticação JWT
* Banco de Dados NoSQL
* Containers Docker
* Inteligência Artificial Generativa
* Cache de Requisições com React Query

---

## 👨‍💻 Autor

**Isac Andrade**



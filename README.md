# Gmail AI Backend

Backend desenvolvido com FastAPI para gerenciamento de agentes de IA integrados ao Gmail.

O sistema permite registrar agentes, autenticar contas Gmail via OAuth2, ler emails, enviar mensagens, gerar resumos automáticos com IA e responder emails automaticamente utilizando OpenAI.

---

# Funcionalidades

## Entregável 1 — Registro de Agente de IA

- Cadastro de agentes via API REST
- Validação de dados com Pydantic
- Criptografia de credenciais Gmail
- Persistência em PostgreSQL
- Arquitetura backend modular
- Deploy em nuvem
- Documentação automática Swagger

---

## Entregável 2 — Automação Inteligente de Emails

- Integração com Gmail API
- Leitura de emails da caixa de entrada
- Envio de emails
- Resumo automático de emails com IA
- Encaminhamento de resumos
- Respostas automáticas inteligentes
- Integração com OpenAI
- OAuth2 Google
- Processamento automatizado de emails

---

# Tecnologias Utilizadas

- Python
- FastAPI
- PostgreSQL
- Neon PostgreSQL
- SQLAlchemy
- Pydantic
- OpenAI API
- Gmail API
- OAuth2 Google
- Cryptography (Fernet)
- Render

---

# Estrutura do Projeto

```text
gmail-ai-backend/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# Arquitetura

O projeto utiliza arquitetura em camadas:

```text
Routes
↓
Services
↓
Database Layer
↓
PostgreSQL
```

Separando:
- regras de negócio
- integração com APIs externas
- persistência
- validações
- segurança
- rotas HTTP

---

# Funcionalidades da API

## Registro de Agente

Endpoint responsável por cadastrar agentes de IA.

### Endpoint

```http
POST /agents
```

### Exemplo de Request

```json
{
  "name": "Agente Financeiro",
  "email_gmail": "agent@gmail.com",
  "client_id": "google-client-id",
  "client_secret": "google-client-secret",
  "refresh_token": "google-refresh-token"
}
```

### Exemplo de Response

```json
{
  "id": 1,
  "name": "Agente Financeiro",
  "email_gmail": "agent@gmail.com",
  "message": "Agent created successfully"
}
```

---

## Ler Emails

### Endpoint

```http
GET /emails/latest/{agent_id}
```

Retorna os emails mais recentes da caixa de entrada.

---

## Enviar Email

### Endpoint

```http
POST /emails/send
```

### Exemplo de Request

```json
{
  "agent_id": 1,
  "receiver": "user@email.com",
  "subject": "Teste",
  "body": "Mensagem enviada pelo sistema."
}
```

---

## Resumir e Encaminhar Email com IA

### Endpoint

```http
POST /emails/summarize-and-forward
```

### Exemplo de Request

```json
{
  "agent_id": 1,
  "message_id": "MESSAGE_ID",
  "forward_to": "manager@email.com"
}
```

---

## Resposta Automática com IA

### Endpoint

```http
POST /emails/auto-reply
```

### Exemplo de Request

```json
{
  "agent_id": 1,
  "message_id": "MESSAGE_ID"
}
```

---

# Segurança

As credenciais sensíveis:
- client_secret
- refresh_token

são criptografadas utilizando:

```python
Fernet
```

da biblioteca:

- Cryptography

---

# Banco de Dados

O sistema utiliza PostgreSQL hospedado no:

- Neon PostgreSQL

Tabela principal:

```text
agents
```

Campos:
- id
- name
- email_gmail
- client_id
- encrypted_client_secret
- encrypted_refresh_token
- created_at

---

# Deploy

A aplicação está hospedada na plataforma:

- Render

---

# Como Executar Localmente

## 1. Clonar repositório

```bash
git clone https://github.com/grazimartins/gmail-ai-backend.git
```

---

## 2. Criar ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Variáveis de Ambiente

Criar arquivo:

```text
.env
```

Baseado em:

```text
.env.example
```

---

## Exemplo

```env
DATABASE_URL=YOUR_DATABASE_URL

SECRET_KEY=YOUR_SECRET_KEY

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

---

# Gerar chave de criptografia

Execute:

```python
from cryptography.fernet import Fernet

print(Fernet.generate_key().decode())
```

---

# Executar aplicação

```bash
uvicorn app.main:app --reload
```

---

# Documentação Swagger

## Produção

:contentReference[oaicite:0]{index=0}

---

# Deploy Produção

Deploy realizado utilizando:

- Render
- Neon PostgreSQL

---

# Próximos Passos

- Background tasks
- Processamento assíncrono
- Filas com Celery/RabbitMQ
- Logs estruturados
- Monitoramento
- Dockerização completa
- Testes automatizados
- Clean Architecture
- Deploy CI/CD

---

# Objetivo do Projeto

Desenvolver uma plataforma backend moderna para automação inteligente de emails utilizando IA generativa, FastAPI e integração com Gmail API.

---

# Autor

Graziene Viana Martins
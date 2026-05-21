# Gmail AI Backend

Backend desenvolvido com FastAPI para gerenciamento de agentes de IA integrados ao Gmail.

O sistema permite registrar agentes com credenciais Gmail de forma segura, realizar leitura de emails, envio de mensagens, respostas automáticas com IA e resumos automáticos utilizando OpenAI.

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

## Entregável 2 — Ações Automatizadas com IA

### Resumo Automático e Encaminhamento

- Leitura de emails Gmail
- Geração de resumo utilizando OpenAI
- Encaminhamento automático do resumo por email

### Resposta Automática Inteligente

- Leitura de emails recebidos
- Geração automática de resposta utilizando IA
- Envio automático de resposta ao remetente original

---

## Entregável 3 — Gerenciamento de Emails

### Leitura de Emails

- Recuperação dos emails mais recentes
- Retorno com:
  - remetente
  - assunto
  - conteúdo
- Limite configurável de emails

### Envio de Emails

- Envio simples de emails
- Validação dos campos de entrada
- Integração completa com Gmail API

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
- Google OAuth2
- google-api-python-client
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
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
├── runtime.txt
├── .env.example
└── README.md
```

---

# Arquitetura

O projeto utiliza arquitetura modular baseada em separação de responsabilidades:

```text
Routes
↓
Services
↓
Utils
↓
Database / External APIs
```

Separando:
- regras de negócio
- persistência
- validações
- segurança
- integrações externas
- rotas HTTP

---

# Endpoints Disponíveis

## Health Check

```http
GET /health
```

---

## Registro de Agente

```http
POST /agents
```

---

## Ler Emails Recentes

```http
GET /emails/latest/{agent_id}?limit=10
```

---

## Enviar Email

```http
POST /emails/send
```

---

## Resumir e Encaminhar Email

```http
POST /emails/summarize-and-forward
```

---

## Resposta Automática com IA

```http
POST /emails/auto-reply
```

---

# Exemplo — Registro de Agente

## Request

```json
{
  "name": "Agente Financeiro",
  "email_gmail": "agent@gmail.com",
  "client_id": "google-client-id",
  "client_secret": "google-client-secret",
  "refresh_token": "google-refresh-token"
}
```

---

## Response

```json
{
  "id": 1,
  "name": "Agente Financeiro",
  "email_gmail": "agent@gmail.com",
  "message": "Agent created successfully"
}
```

---

# Exemplo — Enviar Email

## Request

```json
{
  "agent_id": 1,
  "receiver": "client@email.com",
  "subject": "Teste",
  "body": "Mensagem enviada pela API"
}
```

---

## Response

```json
{
  "message_id": "19e3301269768159",
  "status": "Email sent successfully"
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

## Local

```text
http://localhost:8000/docs
```

---

## Produção

```text
https://gmail-ai-backend-vvtu.onrender.com/docs
```

---

# Deploy Produção

Deploy realizado utilizando:
- Render
- Neon PostgreSQL

---

# Próximas Melhorias

- Background tasks
- Scheduler para leitura automática inbox
- Logs estruturados
- Testes automatizados
- Dockerização completa
- Redis/Celery
- Monitoramento de emails em tempo real
- Classificação automática de emails com IA

---

# Objetivo do Projeto

Desenvolver uma plataforma backend moderna para automação inteligente de emails utilizando IA generativa, FastAPI e integração com Gmail API.

---

# Autor

Graziene Viana Martins
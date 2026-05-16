# Gmail AI Backend

Backend desenvolvido com FastAPI para gerenciamento de agentes de IA integrados ao Gmail.

O sistema permite registrar agentes com credenciais Gmail de forma segura, utilizando criptografia para armazenamento de informações sensíveis.

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

# Tecnologias Utilizadas

- Python
- FastAPI
- PostgreSQL
- Neon PostgreSQL
- SQLAlchemy
- Pydantic
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
│   └── main.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# Arquitetura

O projeto utiliza arquitetura em camadas:

```text
Route
↓
Service
↓
Repository
↓
Database
```

Separando:
- regras de negócio
- persistência
- validações
- segurança
- rotas HTTP

---

# Funcionalidade Atual

## Registro de Agente

Endpoint responsável por cadastrar agentes de IA.

### Endpoint

```http
POST /agents
```

---

# Exemplo de Request

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

# Exemplo de Response

```json
{
  "id": 1,
  "name": "Agente Financeiro",
  "email_gmail": "agent@gmail.com",
  "message": "Agent created successfully"
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
venv\\Scripts\\activate
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

Após iniciar a aplicação:

```text
http://localhost:8000/docs
```

---

# Deploy Produção

Deploy realizado utilizando:

- Render
- Neon PostgreSQL

---

## Documentação da API

https://gmail-ai-backend-vvtu.onrender.com/docs
---

# Próximos Entregáveis

- Leitura de emails Gmail
- Envio de emails
- Resumo automático com IA
- Respostas automáticas inteligentes
- Integração com LLMs
- OAuth2 Google
- Background tasks
- Dockerização completa

---

# Objetivo do Projeto

Desenvolver uma plataforma backend moderna para automação inteligente de emails utilizando IA generativa, FastAPI e integração com Gmail API.

---

# Autor

Graziene Viana Martins
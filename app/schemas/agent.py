from pydantic import BaseModel, EmailStr

# Criar schema (entrada da API)
class AgentCreate(BaseModel):
    name: str
    email_gmail: EmailStr
    client_id: str
    client_secret: str
    refresh_token: str
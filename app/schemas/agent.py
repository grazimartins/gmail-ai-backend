from pydantic import BaseModel, EmailStr


class AgentCreate(BaseModel):
    name: str
    email_gmail: EmailStr
    client_id: str
    client_secret: str
    refresh_token: str

class AgentResponse(BaseModel):
    id: int
    name: str
    email_gmail: EmailStr
    message: str
from pydantic import BaseModel, EmailStr
from typing import List

class EmailResponse(BaseModel):

    id: str
    sender: str
    subject: str
    body: str
    

class SendEmailResponse(BaseModel):

    message_id: str
    status: str


class SendEmailRequest(BaseModel):

    agent_id: int
    receiver: EmailStr
    subject: str
    body: str


class SummarizeAndForwardRequest(BaseModel):

    agent_id: int
    message_id: str
    forward_to: EmailStr


class SummarizeAndForwardResponse(BaseModel):

    status: str
    summary: str


class AutoReplyRequest(BaseModel):

    agent_id: int
    message_id: str


class AutoReplyResponse(BaseModel):

    status: str
    reply: str


class LatestEmailsResponse(BaseModel):

    total: int
    emails: List[EmailResponse]
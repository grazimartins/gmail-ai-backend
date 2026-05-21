from typing import List

from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from googleapiclient.errors import HttpError

import re 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Agent

from app.schemas.email import (
    SummarizeAndForwardResponse,
    SummarizeAndForwardRequest,
    AutoReplyRequest,
    AutoReplyResponse
)

from app.services.gmail_service import GmailService
from app.services.ai_service import AIService


router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)


@router.get("/latest/{agent_id}")
def get_latest_emails(agent_id: int, db: Session = Depends(get_db)):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    emails = GmailService.list_recent_emails(agent=agent)

    return emails



@staticmethod
def clean_receiver(receiver: str) -> str:

    if not receiver:
        raise ValueError("Receiver is empty")

    # remove quebra de linha e espaços
    receiver = receiver.strip()

    # extrai email se vier "Nome <email>"
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", receiver)

    if match:
        return match.group(0)

    raise ValueError(f"Invalid email format: {receiver}")


@staticmethod
def send_email(agent, receiver: str, subject: str, body: str):

    try:
        service = GmailService.get_gmail_client(agent)

        receiver = GmailService.clean_receiver(receiver)

        body = GmailService.clean_email(body)

        message = MIMEText(body, "plain", "utf-8")

        message["To"] = receiver
        message["Subject"] = subject.strip()

        raw_message = urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        result = service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        return {
            "message_id": result["id"],
            "status": "sent"
        }

    except HttpError as error:
        raise Exception(f"Error sending email: {str(error)}")
    

@router.post("/summarize-and-forward")
def summarize_and_forward(request: SummarizeAndForwardRequest,db: Session = Depends(get_db),
                          response_model=SummarizeAndForwardResponse):

    agent = db.query(Agent).filter(
        Agent.id == request.agent_id
    ).first()

    email_data = GmailService.get_email_by_id(
        agent=agent,
        message_id=request.message_id
    )

    summary = AIService.summarize_email(
        email_data["body"]
    )

    GmailService.send_email(
        agent=agent,
        receiver=request.forward_to,
        subject=f"Summary: {email_data['subject']}",
        body=summary
    )

    return {
        "status": "Summary forwarded successfully",
        "summary": summary
    }



@router.post("/auto-reply")
def auto_reply(request: AutoReplyRequest,db: Session = Depends(get_db),
               response_model= AutoReplyResponse):

    agent = db.query(Agent).filter(
        Agent.id == request.agent_id
    ).first()

    email_data = GmailService.get_email_by_id(
        agent=agent,
        message_id=request.message_id
    )

    ai_reply = AIService.generate_email_reply(email_data["body"])

    GmailService.send_email(
        agent=agent,
        receiver=email_data["sender_email"],  # 👈 ISSO AQUI É O FIX
        subject=f"Re: {email_data['subject']}",
        body=ai_reply
    )
        
    return {
        "status": "Auto reply sent successfully",
        "reply": ai_reply
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Agent
from app.utils.agent_utils import get_agent_or_404

from app.schemas.email import (
    LatestEmailsResponse,
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


@router.get("/latest/{agent_id}", response_model=LatestEmailsResponse)
def get_latest_emails(
    agent_id: int, 
    limit: int = 10,
    db: Session = Depends(get_db)
):

    agent = get_agent_or_404(
        db,
        agent_id
    ) 

    emails = GmailService.list_recent_emails(agent=agent, limit=limit)

    return {
        "total": len(emails),
        "emails": emails
    }

 

@router.post(
        "/summarize-and-forward", 
        response_model=SummarizeAndForwardResponse
)
def summarize_and_forward(
    request: SummarizeAndForwardRequest,
    db: Session = Depends(get_db)
):

    agent = get_agent_or_404(
        db,
        request.agent_id
    ) 

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



@router.post(
        "/auto-reply",  
        response_model= AutoReplyResponse,
        status_code=201
)
def auto_reply(
    request: AutoReplyRequest,
    db: Session = Depends(get_db)
):

    agent = get_agent_or_404(
        db,
        request.agent_id
    )

    email_data = GmailService.get_email_by_id(
        agent=agent,
        message_id=request.message_id
    )

    ai_reply = AIService.generate_email_reply(email_data["body"])

    GmailService.send_email(
        agent=agent,
        receiver=email_data["sender_email"],
        subject=f"Re: {email_data['subject']}",
        body=ai_reply
    )
        
    return {
        "status": "Auto reply sent successfully",
        "reply": ai_reply
    }

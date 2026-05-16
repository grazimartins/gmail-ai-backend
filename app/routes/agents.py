from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Agent
from app.schemas.agent import AgentCreate
from app.core.crypto import encrypt

router = APIRouter()


@router.post("/agents")
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):

    agent = Agent(
        name=payload.name,
        email_gmail=payload.email_gmail,
        client_id=payload.client_id,
        client_secret=encrypt(payload.client_secret),
        refresh_token=encrypt(payload.refresh_token)
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "id": agent.id,
        "name": agent.name,
        "email_gmail": agent.email_gmail,
        "message": "Agent created successfully"
    }
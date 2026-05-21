from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Agent


def get_agent_or_404(
    db: Session,
    agent_id: int
):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agent
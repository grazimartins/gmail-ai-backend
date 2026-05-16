from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.database import Base

# Define a tabela agents usando uma classe Python
class Agent(Base):

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email_gmail = Column(
        String,
        unique=True,
        nullable=False
    )

    client_id = Column(String, nullable=False)

    client_secret = Column(String, nullable=False)

    refresh_token = Column(String, nullable=False)
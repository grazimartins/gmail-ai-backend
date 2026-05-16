from fastapi import FastAPI
from app.routes.agents import router as agents_router
from app.db.database import Base, engine
from app.db.models import Agent

Base.metadata.create_all(bind=engine)

print("Tabelas criadas!")


app = FastAPI()

app.include_router(agents_router)
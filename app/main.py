from fastapi import FastAPI
from app.routes.agents import router as agents_router
from app.db.database import Base, engine
from app.db.models import Agent
from app.routes.emails import router as email_router


Base.metadata.create_all(bind=engine)

print("Tabelas criadas!")


app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(agents_router)
app.include_router(email_router)
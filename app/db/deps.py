from app.db.database import SessionLocal

# Criar conexão com o banco de dados para cada requisição da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
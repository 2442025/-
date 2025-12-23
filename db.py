from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from variables import DATABASE_URL

# engine と session ファクトリ
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, future=True)

def get_session():
    return SessionLocal()

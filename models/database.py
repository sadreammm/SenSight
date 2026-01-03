from sqlalchemy import create_engine, Column, String, Integer, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime
from config.settings import settings

Base = declarative_base()

class CodeReview(Base):
    __tablename__ = 'code_reviews'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    repo = Column(String, index=True)
    pr_number = Column(Integer, index=True)
    pr_data = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
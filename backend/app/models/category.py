from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
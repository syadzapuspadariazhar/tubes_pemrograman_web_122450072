from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    deskripsi = Column(String, nullable=False)
    jumlah = Column(Float, nullable=False)
    jenis = Column(String, nullable=False)
    tanggal = Column(Date, nullable=False)
    kategori_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category")

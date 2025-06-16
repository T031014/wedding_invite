# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

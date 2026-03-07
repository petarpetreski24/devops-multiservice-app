from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    in_stock: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    in_stock: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    in_stock: bool
    created_at: datetime

    class Config:
        from_attributes = True

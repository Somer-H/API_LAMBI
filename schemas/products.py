from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    amount: float
    category: Optional[str]
    image: Optional[str]
    standid: int
    
    class Config:
        orm_mode = True
class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    amount: Optional[float]
    category: Optional[str]
    image: Optional[str]

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    idproduct: int

    class Config:
        orm_mode = True
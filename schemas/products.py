from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    amount: float
    category: int
    image: Optional[str]
    standid: int
    
    class Config:
        orm_mode = True
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None 
    price: Optional[float] = None 
    amount: Optional[float] = None
    category: Optional[int] = None
    image: Optional[str] = None
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    idproduct: int

    class Config:
        orm_mode = True
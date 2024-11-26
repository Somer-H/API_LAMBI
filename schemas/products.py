from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    amount: int
    category: int
    image: Optional[List[str]]
    standid: int
    
    class Config:
        orm_mode = True
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None 
    price: Optional[float] = None 
    amount: Optional[int] = None
    category: Optional[int] = None
    image: Optional[List[str]] = None
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    idproduct: int
    class Config:
        orm_mode = True
class CategoryProduct(BaseModel): 
    category: str
    class Config: 
        orm_mode = True
class CategoryProductResponse(BaseModel): 
    idcategoryproduct: int
    category : str
    class Config: 
        orm_mode = True        
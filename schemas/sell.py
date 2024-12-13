from pydantic import BaseModel
from typing import Optional, List

class Sell(BaseModel): 
    hour: str
    date: str
    description: str
    standid_fk: int
    idbuyer: int
    direccion_entrega: str
    class Config:
        orm_mode = True
class SellProduct(BaseModel):
    idsell: int 
    idproduct: int  
    amount: int
class SellProductResponseNow(BaseModel):
    idsell: int
    idproduct: int  
    amount: int
    date: str
    sell_description: str
    hour: str
    idbuyer: int
    standid_fk: int
    category: int
    name : str 
    product_description: str
    image: List[Optional[str]] = None
    price: float
    total_price: float
    direccion_entrega: str
class SellProductRequest(BaseModel):
    idproduct: int
    amount: int
class SellRequest(BaseModel): 
    hour: str
    date: str
    description: str
    standid_fk: int
    idbuyer: int
    direccion_entrega: str
    sells: List[SellProductRequest]
class CreateSellProduct(SellProduct): 
    pass          
class CreateSell(Sell): 
    pass
class UpdateSell(BaseModel):
    hour: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    direccion_entrega: Optional[str] = None
class SellResponse(Sell): 
    idsell: int              
class SellProductResponse(BaseModel):
    sell: SellResponse
    sells: List[SellProduct]
    total_price: float
    class Config:
        orm_mode = True
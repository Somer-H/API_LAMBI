from pydantic import BaseModel
from typing import Optional, List

class Sell(BaseModel): 
    hour: str
    date: str
    description: str
    standid_fk: int
    idbuyer: int
    class Config:
        orm_mode = True
class SellProduct(BaseModel):
    idsell: int 
    idproduct: int  
    amount: int
class SellProductRequest(BaseModel):
    idproduct: int
    amount: int
class SellRequest(BaseModel): 
    hour: str
    date: str
    description: str
    standid_fk: int
    idbuyer: int
    sells: List[SellProductRequest]
class CreateSellProduct(SellProduct): 
    pass          
class CreateSell(Sell): 
    pass
class UpdateSell(BaseModel):
    hour: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
class SellResponse(Sell): 
    idsell: int              
class SellProductResponse(BaseModel):
    sell: SellResponse
    sells: List[SellProduct]
    total_price: float
    class Config:
        orm_mode = True
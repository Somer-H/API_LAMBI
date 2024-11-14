from pydantic import BaseModel
from typing import Optional

class Sell(BaseModel): 
    hour: str
    date: str
    description: str
    sellerid: int
    idbuyer: int
    class Config:
        orm_mode = True
class CreateSell(Sell): 
    pass
class UpdateSell(BaseModel):
    hour: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
class SellResponse(Sell): 
    idsell: int    
from pydantic import BaseModel
from typing import Optional

class FavoriteBase(BaseModel):
    idBuyer: int
    idProduct: int
    
    class Config:
        orm_mode = True

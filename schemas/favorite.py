from pydantic import BaseModel
from typing import Optional

class FavoriteBase(BaseModel):
    iduser: int
    idstand: int
    class Config:
        orm_mode = True
class FavoriteResponse(FavoriteBase): 
    status: bool        
    class Config:
        orm_mode = True
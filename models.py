from pydantic import BaseModel
from typing import Optional, List
from schemas.stand import Adress
class SellerResponse(BaseModel):
    name: str
    lastname: str
    e_mail: str
    password: str
    
class StandResponse(BaseModel):
    name: str
    description: str
    image: Optional[str]
    category: str
    location: List[Adress]
    horario: str
    phone: List[str]
    iduser: int

class Config:
        orm_mode = True
class Config:
        orm_mode = True        
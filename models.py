from pydantic import BaseModel
from typing import Optional
class SellerResponse(BaseModel):
    iduser: Optional[int]
    name: str
    lastname: str
    e_mail: str
    password: str
    
    
class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import Optional
class SellerResponse(BaseModel):
    name: str
    lastname: str
    e_mail: str
    password: str
    
    
class Config:
        orm_mode = True
class Config:
        orm_mode = True        
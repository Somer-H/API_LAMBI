from pydantic import BaseModel
from typing import Optional
class BuyerBase(BaseModel):
    name: str
    lastname: str
    e_mail: str
    password: str

class BuyerLogin(BaseModel):
    e_mail: str
    password: str

class BuyerUpdate(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
class BuyerResponseGet(BaseModel):
    idbuyer: int
    name: str
    lastname: str
    
class BuyerLoginResponse(BaseModel):
    idbuyer: int
    name: str

class BuyerUpdateResponse(BaseModel):
    idbuyer: int
    name: str
    lastname: str

    class Config:
        orm_mode = True

class BuyerCreate(BuyerBase):
    pass

class Buyer(BuyerBase):
    iduser: int

    class Config:
        orm_mode = True
class RateBase(BaseModel): 
    idstand: int
    idbuyer: int 
    stars: int
    class Config: 
        orm_mode = True        
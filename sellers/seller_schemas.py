from pydantic import BaseModel
from typing import Optional
class SellerBase(BaseModel):    
    name: str
    lastname: str
    e_mail: str
    password: str

    class Config:
        orm_mode = True

class SellerRequest(SellerBase):
    pass

class SellerResponse(SellerBase):
    iduser: int

    class Config:
        orm_mode = True
class SellerUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    e_mail: Optional[str] = None
    password: Optional[str] = None
class SellerUpdateRequest(SellerUpdate):
    pass
    class Config:
        orm_mode = True
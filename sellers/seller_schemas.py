from pydantic import BaseModel

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
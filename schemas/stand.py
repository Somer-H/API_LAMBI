from pydantic import BaseModel
from typing import Optional

class Adress(BaseModel):
    street: str
    no_house: str
    colonia: Optional[str]
    municipio: Optional[str]
    estado: Optional[str]
    latitud: Optional[str]
    altitud: Optional[str]

    class Config:
        orm_mode = True

class StandBase(BaseModel):
    name: str
    description: str
    image: Optional[str]
    category: Optional[str]
    location: Optional[Adress]
    horario: str
    phone: str
    idseller: int

    class Config:
        orm_mode = True

class StandCreate(StandBase):
    pass

class Stand(StandBase):
    idstand: int

    class Config:
        orm_mode = True

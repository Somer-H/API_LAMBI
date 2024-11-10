from pydantic import BaseModel
from typing import Optional
from typing import List
class Adress(BaseModel):
    street: str
    no_house: Optional[str]
    colonia: str
    municipio: str
    estado: str
    latitud: Optional[str]
    altitud: Optional[str]

    class Config:
        orm_mode = True

class StandBase(BaseModel):
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

class StandCreate(StandBase):
    pass
class StandResponse(StandBase):
    iduser: int
    class Config:
        orm_mode = True

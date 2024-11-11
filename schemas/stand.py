from pydantic import BaseModel
from typing import Optional
from typing import List
class StandBase(BaseModel):
    name: str
    description: str
    image: Optional[str]
    category: str
    street: str
    no_house: str
    colonia: str
    municipio: str
    estado: str
    latitud: str
    altitud: str
    horario: str
    phone: List[str]
    idseller: int
    class Config:
        orm_mode = True

class StandCreate(StandBase):
    pass
class StandResponse(StandBase):
    idstand: int
    class Config:
        orm_mode = True

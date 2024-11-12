from pydantic import BaseModel
from typing import Optional
from typing import List
class CategoryBase(BaseModel): 
    category: str
    class Config:
        orm_mode = True
class Catetory(CategoryBase):
    pass  
class CategoryResponse(CategoryBase):
    idcategory: int      
class StandSellerResponse(BaseModel): 
    idstand: int
    stand_name: str
    description: str
    image: str
    horario: str
    phone: List[str]
    idseller: int
    street: str
    no_house: str
    colonia: str
    municipio: str
    estado: str
    latitud: str
    altitud: str
    category: int
    seller_name: str
    seller_lastname: str

class StandBase(BaseModel):
    name: str
    description: str
    image: Optional[str]
    category: int
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
class StandUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    image: Optional[str]
    category: Optional[int]
    street: Optional[str]
    no_house: Optional[str]
    colonia: Optional[str]
    municipio: Optional[str]
    estado: Optional[str]
    latitud: Optional[str]
    altitud: Optional[str]
    horario: Optional[str]
class StandCreate(StandBase):
    pass
class StandResponse(StandBase):
    idstand: int
    class Config:
        orm_mode = True

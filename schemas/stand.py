from pydantic import BaseModel
from typing import Optional
from typing import List
from fastapi import Form
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
    image: List[str]
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
    image: Optional[List[str]]
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
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[List[str]] = None
    category: Optional[int] = None 
    street: Optional[str] = None 
    no_house: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None 
    latitud: Optional[str]= None 
    altitud: Optional[str] = None
    horario: Optional[str] = None 
class StandCreate(StandBase):
    pass
class StandResponse(StandBase):
    idstand: int
    class Config:
        orm_mode = True

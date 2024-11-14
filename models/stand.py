from sqlalchemy import Column, Integer, String, ARRAY,ForeignKey, Float
from databasecontent.database import Base
from sqlalchemy import Column, Integer, String
from databasecontent.database import Base

class Stand(Base):
    __tablename__ = "stand"

    idstand = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(ARRAY(String), nullable=False)
    category = Column(Integer, nullable=True)
    horario = Column(String, nullable=True)
    phone = Column(ARRAY(String), nullable=True)
    idseller = Column(Integer, ForeignKey('Seller.iduser'), nullable=True)
    street = Column (String, nullable = True)
    no_house = Column(Integer, nullable = False)
    colonia = Column(String, nullable = True)
    municipio = Column(String, nullable = True)
    estado = Column(String, nullable = True)
    latitud = Column(Float, nullable = True)
    altitud = Column(Float, nullable = True)
class CategoryModel(Base): 
    __tablename__ = 'Category'
    idcategory = Column(Integer, primary_key= True, nullable = True, autoincrement= True)
    category = Column(String, nullable = True)

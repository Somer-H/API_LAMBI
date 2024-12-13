from sqlalchemy import Column, Integer, String, Float, ARRAY, ForeignKey
from databasecontent.database import Base 

class Product(Base):
    __tablename__ = "product"

    idproduct = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    amount = Column(Integer, nullable=True)
    category = Column(Integer,ForeignKey('CategoryProduct.idcategoryproduct'), nullable=True)
    image = Column(ARRAY(String), nullable=True)
    standid = Column(Integer,ForeignKey('stand.idstand'), nullable=False)
class CategoryBase(Base): 
    __tablename__ = "CategoryProduct"
    idcategoryproduct = Column(Integer, primary_key=True, nullable=False)
    category = Column(String, nullable=False)
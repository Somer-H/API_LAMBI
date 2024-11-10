from sqlalchemy import Column, Integer, String,Float
from databasecontent.database import Base 

class Product(Base):
    __tablename__ = "product"

    idproduct = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    category = Column(String, nullable=True)
    image = Column(String, nullable=True)
    sellerid = Column(Integer, nullable=False)

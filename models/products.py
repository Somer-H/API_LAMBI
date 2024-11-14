from sqlalchemy import Column, Integer, String, Float, ARRAY
from databasecontent.database import Base 

class Product(Base):
    __tablename__ = "product"

    idproduct = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)  # Permitir nulos
    price = Column(Float, nullable=True)  # Permitir nulos
    amount = Column(Integer, nullable=True)  # Permitir nulos
    category = Column(Integer, nullable=True)  # Permitir nulos
    image = Column(ARRAY(String), nullable=True)  # Permitir nulos
    standid = Column(Integer, nullable=False)

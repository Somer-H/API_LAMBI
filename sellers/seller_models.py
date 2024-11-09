from sqlalchemy import Column, Integer, String
from databasecontent.database import Base 

class Seller(Base):
    __tablename__ = "Seller"
    
    iduser = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    e_mail = Column(String, nullable=True)
    password = Column(String, nullable=True)
  
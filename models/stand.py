from sqlalchemy import Column, Integer, String, JSON, ARRAY
from databasecontent.database import Base

class Stand(Base):
    __tablename__ = "stand"

    idstand = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    category = Column(String, nullable=True)
    horario = Column(String, nullable=True)
    phone = Column(ARRAY(String)) 
    idseller = Column(Integer, nullable=True)
    location = Column(JSON, nullable=True) 

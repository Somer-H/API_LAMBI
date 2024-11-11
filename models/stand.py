from sqlalchemy import Column, Integer, String, JSON, ARRAY, TypeDecorator
from databasecontent.database import Base
from sqlalchemy import Column, Integer, String, JSON, TypeDecorator
from databasecontent.database import Base

class Stand(Base):
    __tablename__ = "stand"

    idstand = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    category = Column(String, nullable=True)
    horario = Column(String, nullable=True)
    phone = Column(ARRAY(String), nullable=True)
    idseller = Column(Integer, nullable=True)
    street = Column (String, nullable = True)
    no_house = Column(Integer, nullable = False)
    colonia = Column(String, nullable = True)
    municipio = Column(String, nullable = True)
    estado = Column(String, nullable = True)
    latitud = Column(String, nullable = True)
    altitud = Column(String, nullable = True)
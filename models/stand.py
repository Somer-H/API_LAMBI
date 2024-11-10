from sqlalchemy import Column, Integer, String, JSON, ARRAY
from databasecontent.database import Base
from sqlalchemy.orm import validates
import json

class Stand(Base):
    __tablename__ = "stand"

    idstand = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    category = Column(String, nullable=True)
    horario = Column(String, nullable=True)
    phone = Column(ARRAY(String), nullable=True)
    iduser = Column(Integer, nullable=True)
    location = Column(ARRAY(JSON))

    @validates('location')
    def convert_location(self, key, value):
        if isinstance(value, str):
            return json.loads(value)  # Convierte la cadena JSON en un objeto Python
        return value
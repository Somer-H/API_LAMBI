from sqlalchemy import Column, Integer, String, JSON, ARRAY, TypeDecorator
from databasecontent.database import Base
from sqlalchemy.orm import validates
from schemas.stand import Adress
import types
from sqlalchemy import Column, Integer, String, JSON, TypeDecorator
from databasecontent.database import Base
from sqlalchemy.orm import validates
import json

# Define el tipo personalizado para manejar "Address" como un objeto JSON en la base de datos.
class AddressType(TypeDecorator):
    """Tipo personalizado para manejar el tipo 'address' en la base de datos."""
    impl = JSON  # Utilizamos el tipo JSON de la base de datos directamente

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Serializar el diccionario a una cadena JSON antes de insertarlo
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # Deserializar la cadena JSON de la base de datos a un diccionario
            return json.loads(value)
        return value
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
    location = Column(ARRAY(AddressType))
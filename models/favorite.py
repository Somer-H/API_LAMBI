from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from databasecontent.database import Base 

class Favorite(Base):
    __tablename__ = "favorite"

    iduser = Column(Integer, ForeignKey('Buyer.iduser'), primary_key=True, nullable=True)
    idstand = Column(Integer, ForeignKey('stand.idstand'), primary_key=True, nullable=True)
    status = Column(Boolean, nullable=True)

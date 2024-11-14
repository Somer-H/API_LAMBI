from sqlalchemy import Column, Integer, String, ForeignKey
from databasecontent.database import Base 

class Favorite(Base):
    __tablename__ = "favorite"

    iduser = Column(Integer, ForeignKey('Buyer.iduser'), nullable=True)
    idStand = Column(Integer, ForeignKey('stand.idstand'), nullable=True)


from sqlalchemy import Column, Integer, String, ForeignKey
from databasecontent.database import Base 

class Buyer(Base):
    __tablename__ = "Buyer"
    
    iduser = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    e_mail = Column(String, nullable=True)
    password = Column(String, nullable=True)
class RateModel(Base): 
    __tablename__ = 'rate'
    idstand = Column(Integer, ForeignKey('stand.idstand'), primary_key= True, nullable = True)
    idbuyer = Column(Integer, ForeignKey('Buyer.iduser'), primary_key= True, nullable = True)
    stars = Column(Integer, nullable = True)

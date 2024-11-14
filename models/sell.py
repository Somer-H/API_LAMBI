from sqlalchemy import Column, Integer, String, ARRAY,ForeignKey
from databasecontent.database import Base
from sqlalchemy import Column, Integer, String
from databasecontent.database import Base

class SellModel(Base): 
     __tablename__ = "sell"

     idsell = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
     hour = Column(String, nullable = True)
     date = Column(String, nullable = True)
     description = Column(String, nullable = True)
     sellerid = Column(Integer, ForeignKey('Seller.iduser'), nullable=True)
     idbuyer = Column(Integer, ForeignKey('Buyer.iduser'), nullable=True)
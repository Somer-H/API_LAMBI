from sqlalchemy import Column, Integer, String, ARRAY,ForeignKey
from databasecontent.database import Base
from sqlalchemy import Column, Integer, String, Float
from databasecontent.database import Base

class SellModel(Base): 
     __tablename__ = "sell"

     idsell = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
     hour = Column(String, nullable = True)
     date = Column(String, nullable = True)
     description = Column(String, nullable = True)
     standid_fk = Column(Integer, ForeignKey('Seller.iduser'), nullable=True)
     idbuyer = Column(Integer, ForeignKey('Buyer.iduser'), nullable=True)
     total_price = Column(Float, nullable = True)
     direccion_entrega = Column(String, nullable = True)

class SellProduct(Base): 
     __tablename__ = "sellproduct"
     idsell = Column(Integer, ForeignKey('sell.idsell'),primary_key=True, nullable=True)
     idproduct = Column(Integer, ForeignKey('product.idproduct'),primary_key=True, nullable = True)
     amount = Column(Integer, nullable = True)

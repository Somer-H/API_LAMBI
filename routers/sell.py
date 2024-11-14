from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from databasecontent.database import get_db
from typing import List
from models.sell import SellModel
from sellers.seller_models import Seller
from schemas.sell import SellResponse, CreateSell, UpdateSell, SellProduct
sell_router = APIRouter()
@sell_router.post("/sell", status_code=status.HTTP_201_CREATED, response_model=SellResponse)
def create_sell(stand: CreateSell, db: Session = Depends(get_db)):
 
  try:
        new_sell = SellModel(**stand.dict())
        db.add(new_sell)
        db.commit()
        db.refresh(new_sell)
        return new_sell
  except HTTPException as e:
        raise e
    
  except Exception as e:
        print("Error durante el registro del producto:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
@sell_router.get("sell", status_code=status.HTTP_200_OK, response_model=List[SellResponse])
def get_sell(db: Session = Depends(get_db)):
     all_sells = db.query(SellModel).all()
     return all_sells  
@sell_router.put("/sell/{idsell}", status_code=status.HTTP_201_CREATED, response_model=SellResponse | bool)
def put_sell(idsell: int, sell_update: UpdateSell, db: Session = Depends(get_db)):
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if not sell:
        raise HTTPException(status_code=404, detail="Seller not found")
        return False
    updated = False
    if sell_update.date is not None:
        sell.date = sell_update.date
        updated = True
    if sell_update.hour is not None:
        sell.hour = sell_update.hour
        updated = True
    if sell_update.description is not None:
        sell.description = sell.description
        updated = True       
    if updated:
        try:
            db.commit()
            db.refresh(sell)
            return sell
        except Exception as e:
            db.rollback()
            return sell
@sell_router.delete("/sell/{idsell}", status_code=status.HTTP_200_OK, response_model= bool)
def delete_sell(idsell: int, db: Session = Depends(get_db)):
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if sell :
       db.delete(sell)
       db.commit()
       return True
    else :
        return False        
@sell_router.get("/sell/{idsell}", status_code=status.HTTP_200_OK, response_model=SellResponse | bool)
def get_sell_byId(idsell: int, db: Session = Depends(get_db)): 
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if(sell): 
        return sell
    else: 
        return False
@sell_router.post("/sellProduct", status_code = status.HTTP_201_CREATED, response_model= SellProduct)
def add_sell_product(sell: SellProduct, db: Session = Depends(get_db)): 
    try:
     new_sell = SellModel(**sell.dict())
     db.add(new_sell)
     db.commit
     return new_sell 
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print("Error durante el registro del producto:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
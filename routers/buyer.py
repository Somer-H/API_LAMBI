from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta
from typing import List
import bcrypt
from schemas.buyer import Buyer,BuyerUpdate, BuyerCreate,BuyerResponseGet,BuyerLogin,BuyerLoginResponse,BuyerUpdateResponse
from models.buyer import Buyer as BuyerModel
from databasecontent.database import engine, get_db, Base
buyer_router = APIRouter()

SECRET_KEY = "LAPUERTADELAMBI"
ALGORITHM = "HS256"
@buyer_router.post("/registerBuyer/", response_model=BuyerResponseGet)
async def register_buyer(buyer: BuyerCreate, db: Session = Depends(get_db)):
    try:
        db_buyer = db.query(BuyerModel).filter(BuyerModel.e_mail == buyer.e_mail).first()
        if db_buyer:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = bcrypt.hashpw(buyer.password.encode('utf-8'), bcrypt.gensalt())
        
        new_buyer = BuyerModel(
            name=buyer.name,
            lastname=buyer.lastname,
            e_mail=buyer.e_mail,
            password=hashed_password.decode('utf-8'),
        )

        db.add(new_buyer)
        db.commit()
        db.refresh(new_buyer)

        response = BuyerResponseGet(idbuyer=new_buyer.iduser, name=new_buyer.name, lastname=new_buyer.lastname)
        
        return response
    
    except HTTPException as e:
        raise e 
    
    except Exception as e:
        print("Error durante el registro del comprador:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")

@buyer_router.get("/getAllBuyers/", response_model=List[BuyerResponseGet])
async def get_all_buyers(db: Session = Depends(get_db)):
    return db.query(BuyerModel).all()

@buyer_router.get("/getUserById/{idbuyer}", response_model=Buyer)
async def get_buyer_by_id(idbuyer: int, db: Session = Depends(get_db)):
    buyer = db.query(BuyerModel).filter(BuyerModel.iduser == idbuyer).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer

@buyer_router.post("/loginBuyer/", response_model=BuyerLoginResponse)
async def login_buyer(buyer: BuyerLogin, db: Session = Depends(get_db)):
    db_buyer = db.query(BuyerModel).filter(BuyerModel.e_mail == buyer.e_mail).first()
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Email not found")
    
    
    if not bcrypt.checkpw(buyer.password.encode('utf-8'), db_buyer.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"idbuyer": db_buyer.iduser, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

    response = JSONResponse(content={"idbuyer": db_buyer.iduser, "name": db_buyer.name})
    response.headers["Authorization"] = f"Bearer {token}"

    return response


@buyer_router.put("/updateBuyer/{idbuyer}", response_model=BuyerUpdateResponse)
async def update_buyer(idbuyer: int, buyer: BuyerUpdate, db: Session = Depends(get_db)):
    db_buyer = db.query(BuyerModel).filter(BuyerModel.iduser == idbuyer).first()
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    db_buyer.name = buyer.name
    db_buyer.lastname = buyer.lastname
    
    db.commit()
    db.refresh(db_buyer)
    response = BuyerUpdateResponse(idbuyer=db_buyer.iduser, name=db_buyer.name,lastname=db_buyer.lastname)
    
    return response

@buyer_router.delete("/deleteBuyer/{idbuyer}", response_model=BuyerUpdateResponse)
async def delete_buyer(idbuyer: int, db: Session = Depends(get_db)):
    db_buyer = db.query(BuyerModel).filter(BuyerModel.iduser == idbuyer).first()
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    db.delete(db_buyer)
    db.commit()
    response = BuyerUpdateResponse(idbuyer=db_buyer.iduser, name=db_buyer.name, lastname=db_buyer.lastname)
    
    return response

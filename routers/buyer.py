from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta
from typing import List
import bcrypt
from schemas.buyer import Buyer,BuyerUpdate, BuyerCreate,BuyerResponseGet,BuyerLogin,BuyerLoginResponse,BuyerUpdateResponse, RateBase, RateUpdate
from models.buyer import Buyer as BuyerModel, RateModel
from databasecontent.database import get_db
from schemas.favorite import FavoriteBase, FavoriteResponse
from models.favorite import Favorite
from schemas.stand import StandFavoriteResponse
from models.stand import Stand
buyer_router = APIRouter()
from dotenv import load_dotenv
import os 
load_dotenv()
bearer_scheme = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
@buyer_router.post("/registerBuyer/", response_model=BuyerResponseGet)
async def register_buyer(buyer: BuyerCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el email ya está registrado
        db_buyer = db.query(BuyerModel).filter(BuyerModel.e_mail == buyer.e_mail).first()
        if db_buyer:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Crear el hash de la contraseña
        hashed_password = bcrypt.hashpw(buyer.password.encode('utf-8'), bcrypt.gensalt())
        
        # Crear un nuevo registro de comprador
        new_buyer = BuyerModel(
            name=buyer.name,
            lastname=buyer.lastname,
            e_mail=buyer.e_mail,
            password=hashed_password.decode('utf-8'),
        )

        db.add(new_buyer)
        db.commit()
        db.refresh(new_buyer)

        # Generar el token JWT
        expiration = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode({"idbuyer": new_buyer.iduser, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

        # Preparar la respuesta
        response = JSONResponse(content={
            "idbuyer": new_buyer.iduser,
            "name": new_buyer.name,
            "lastname": new_buyer.lastname
        }, status_code=201)
        
        # Incluir el token en el encabezado
        response.headers["Authorization"] = f"Bearer {token}"

        return response

    except HTTPException as e:
        raise e 
    
    except Exception as e:
        print("Error durante el registro del comprador:", e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")


@buyer_router.get("/all/buyer/", response_model=List[BuyerResponseGet])
async def get_all_buyers(db: Session = Depends(get_db)):
    db_buyers = db.query(BuyerModel).all()
    if not db_buyers:
        raise HTTPException(status_code=404, detail="No buyers found")
    response = [
        BuyerResponseGet(idbuyer=buyer.iduser, name=buyer.name, lastname=buyer.lastname)
        for buyer in db_buyers
    ]
    
    return response

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

    response = JSONResponse(content={"idbuyer": db_buyer.iduser, "name": db_buyer.name}, status_code=200)
    response.headers["Authorization"] = f"Bearer {token}"
    return response


@buyer_router.put("/protected/updateBuyer/{idbuyer}", response_model=BuyerUpdateResponse)
async def update_buyer(idbuyer: int, buyer: BuyerUpdate, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    db_buyer = db.query(BuyerModel).filter(BuyerModel.iduser == idbuyer).first()
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    db_buyer.name = buyer.name
    db_buyer.lastname = buyer.lastname
    
    db.commit()
    db.refresh(db_buyer)
    response = BuyerUpdateResponse(idbuyer=db_buyer.iduser, name=db_buyer.name,lastname=db_buyer.lastname)
    
    return response

@buyer_router.delete("/protected/deleteBuyer/{idbuyer}", response_model=BuyerUpdateResponse)
async def delete_buyer(idbuyer: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    db_buyer = db.query(BuyerModel).filter(BuyerModel.iduser == idbuyer).first()
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    db.delete(db_buyer)
    db.commit()
    response = BuyerUpdateResponse(idbuyer=db_buyer.iduser, name=db_buyer.name, lastname=db_buyer.lastname)
    
    return response
@buyer_router.post("/protected/favorites", status_code=status.HTTP_200_OK, response_model=FavoriteResponse)
def addFavorite(favorite: FavoriteBase, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try: 
        newFavorite = Favorite(**favorite.dict())
        newFavorite.status = True

        db.add(newFavorite)
        db.commit()
        db.refresh(newFavorite)
        print(newFavorite)  # Verificar todos los campos
        return newFavorite
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding favorite: {str(e)}")
@buyer_router.put("/protected/changeToFalse/favorite/{iduser}/{idstand}", status_code=status.HTTP_200_OK, response_model=bool)
def delete_favorite(iduser: int, idstand: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    favorite_search = db.query(Favorite).filter(Favorite.iduser==iduser).filter(Favorite.idstand==idstand).first()
    if(favorite_search):
        favorite_search.status= False
        db.commit()
        db.refresh(favorite_search)
        return True
    else: 
        return False    
@buyer_router.put("/protected/changeToTrue/favorite/{iduser}/{idstand}", status_code=status.HTTP_200_OK, response_model=bool)
def recuperate_favorite(iduser: int, idstand: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    favorite_search = db.query(Favorite).filter(Favorite.iduser==iduser).filter(Favorite.idstand==idstand).first()
    if(favorite_search):
        favorite_search.status= True
        db.commit()
        db.refresh(favorite_search)
        return True
    else: 
        return False    
@buyer_router.post("/protected/rate", status_code=status.HTTP_201_CREATED, response_model=RateBase | bool)
def add_rate(rate : RateBase, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)): 
    new_rate = RateModel(**rate.dict())
    if(new_rate.stars > 5 or new_rate.stars < 0):
        raise HTTPException(status_code=400, detail="Solo puede añadir de 1 a 5 estrellas")
    else:
     db.add(new_rate)
     db.commit()
     return new_rate
@buyer_router.put("/protected/rate", status_code = status.HTTP_200_OK, response_model=RateBase | bool)
def update_rate(idstand: int, idbuyer: int, rate: RateUpdate,db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)): 
    rate_search = db.query(RateModel).filter(RateModel.idstand ==idstand). filter(RateModel.idbuyer == idbuyer).first()
    if(rate_search):
        rate_search.stars = rate.stars
        db.commit()
        db.refresh(rate_search)
        return True
    else:
        return False
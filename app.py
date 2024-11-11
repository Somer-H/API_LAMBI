from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from databasecontent.database import engine, get_db, Base
from sellers.seller_schemas import SellerRequest,SellerLogin, SellerResponse, SellerUpdateRequest, SellerUpdate  # Importación desde sellers/user_schemas.py
from sellers.seller_models import Seller  # Importación desde sellers/user_model.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import bcrypt
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from routers.buyer import buyer_router
from routers.products import product_router
from routers.stand import stand_router
app.include_router(buyer_router, prefix="/api", tags=["users"])
app.include_router(product_router, prefix="/api", tags=["products"])
app.include_router(stand_router, prefix="/api", tags=["stand"])
# Añadir CORS
origins = [
    "http://localhost",  # Ajusta según sea necesario
    "http://localhost:8000",
]
SECRET_KEY = "LAPUERTADELAMBI"
ALGORITHM = "HS256"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return { 'message': 'Server alive!', 'time': datetime.now() }

@app.get('/sellers', status_code=status.HTTP_200_OK, response_model=List[SellerResponse])
def get_all_users(db: Session = Depends(get_db)):
    all_sellers = db.query(Seller).all()
    for seller in all_sellers:
        print(f'ID: {seller.iduser}, Nombre: {seller.name}, Lastaname: {seller.lastname}, E_mail: {seller.e_mail}, Password: {seller.password}')
    return all_sellers

@app.post('/sellers', status_code=status.HTTP_201_CREATED, response_model=SellerResponse)
def create_user(post_user: SellerRequest, db: Session = Depends(get_db)):
    try:
        hashed_password = bcrypt.hashpw(post_user.password.encode('utf-8'), bcrypt.gensalt())

        new_user = Seller(
            name=post_user.name,
            lastname=post_user.lastname,
            e_mail=post_user.e_mail,
            password=hashed_password.decode('utf-8') 
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Error creating seller: " + str(e))

@app.get("/sellers/{iduser}", response_model=SellerResponse)
def get_user(iduser: int, db: Session = Depends(get_db)):
    user = db.query(Seller).filter(Seller.iduser == iduser).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/sellers/{iduser}", status_code=status.HTTP_201_CREATED, response_model=SellerResponse)
def put_user(iduser: int, seller_update: SellerUpdateRequest, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.iduser == iduser).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    updated = False
    if seller_update.e_mail is not None:
        seller.e_mail = seller_update.e_mail
        updated = True
    if seller_update.lastname is not None:
        seller.lastname = seller_update.lastname
        updated = True
    if seller_update.name is not None:
        seller.name = seller_update.name
        updated = True
    if seller_update.password is not None:
        seller.password = seller_update.password
        updated = True
    
    if updated:
        try:
            db.commit()
            db.refresh(seller)
            return seller
        except Exception as e:
            db.rollback()
            return seller
@app.delete("/sellers/{iduser}", status_code=status.HTTP_201_CREATED, response_model= bool)
def delete_user(iduser: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.iduser == iduser).first()
    if seller :
       db.delete(seller)
       db.commit()
       return True
    else :
        return False

@app.post("/loginSeller/", response_model=SellerResponse)
async def login_seller(seller: SellerLogin, db: Session = Depends(get_db)):
    db_seller = db.query(Seller).filter(Seller.e_mail == seller.e_mail).first()
    if not db_seller:
        raise HTTPException(status_code=404, detail="Email not found")
    
    
    if not bcrypt.checkpw(seller.password.encode('utf-8'), db_seller.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"idseller": db_seller.iduser, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

    response = JSONResponse(content={"idseller": db_seller.iduser, "name": db_seller.name})
    response.headers["Authorization"] = f"Bearer {token}"

    return response

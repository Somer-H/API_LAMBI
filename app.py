from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from databasecontent.database import engine, get_db, Base
from sellers.seller_schemas import SellerRequest, SellerResponse  # Importación desde sellers/user_schemas.py
from sellers.seller_models import Seller  # Importación desde sellers/user_model.py
from sqlalchemy.orm import Session
from datetime import datetime
app = FastAPI()
Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware
from routers.buyer import buyer_router
from routers.products import product_router
app.include_router(buyer_router, prefix="/api", tags=["users"])
app.include_router(product_router, prefix="/api", tags=["products"])
# Añadir CORS
origins = [
    "http://localhost",  # Ajusta según sea necesario
    "http://localhost:8000",
]

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
    new_user = Seller(**post_user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    pass
    return new_user.__dict__

@app.get("/sellers/{iduser}", response_model=SellerResponse)
def get_user(iduser: int, db: Session = Depends(get_db)):
    user = db.query(Seller).filter(Seller.iduser == iduser).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
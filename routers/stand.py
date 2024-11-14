from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from databasecontent.database import get_db
from typing import List
from models.stand import Stand as StandModel, CategoryModel
from sellers.seller_models import Seller
from schemas.stand import StandCreate, StandResponse,StandUpdateRequest, Catetory, CategoryResponse, StandSellerResponse
stand_router = APIRouter()

import json

@stand_router.post("/stand", status_code=status.HTTP_200_OK, response_model=StandResponse)
def create_stand(stand: StandCreate, db: Session = Depends(get_db)):
 
  try:
        new_stand = StandModel(**stand.dict())
        db.add(new_stand)
        db.commit()
        db.refresh(new_stand)
        db.commit()
        return new_stand
  except HTTPException as e:
        raise e
    
  except Exception as e:
        print("Error durante el registro del producto:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
@stand_router.get('/stand', status_code=status.HTTP_200_OK, response_model=List[StandResponse])
def get_all_stands(db: Session = Depends(get_db)):
    all_stands = db.query(StandModel).all()
    return all_stands
@stand_router.put("/stand/{idstand}", status_code=status.HTTP_201_CREATED, response_model=StandResponse)
def put_stand(idstand: int, stand_update: StandUpdateRequest, db: Session = Depends(get_db)):
    stand = db.query(StandModel).filter(StandModel.idstand == idstand).first()
    if not stand:
        raise HTTPException(status_code=404, detail="Seller not found")
    updated = False
    if stand_update.altitud is not None:
        stand.altitud = stand_update.altitud
        updated = True
    if stand_update.category is not None:
        stand.category = stand_update.category
        updated = True
    if stand_update.colonia is not None:
        stand.description = stand.description
        updated = True
    if stand_update.municipio is not None:
        stand.municipio = stand_update.municipio
        updated = True
    if stand_update.description is not None:
        stand.description = stand_update.municipio
    if stand_update.estado is not None: 
        stand.estado = stand_update.estado
    if stand_update.horario is not None: 
        stand.horario = stand_update.horario
    if stand_update.image is not None:
        stand.image = stand_update.image         
    if updated:
        try:
            db.commit()
            db.refresh(stand)
            return stand
        except Exception as e:
            db.rollback()
            return stand
@stand_router.delete("/stand/{idstand}", status_code=status.HTTP_200_OK, response_model= bool)
def delete_stand(idstand: int, db: Session = Depends(get_db)):
    stand = db.query(StandModel).filter(StandModel.idstand == idstand).first()
    if stand :
       db.delete(stand)
       db.commit()
       return True
    else :
        return False
@stand_router.get("/stand/{idstand}", status_code=status.HTTP_200_OK, response_model=StandResponse | bool)
def get_stand_byId(idstand: int, db: Session = Depends(get_db)):
    stand = db.query(StandModel).filter(StandModel.idstand == idstand).first()
    if(stand):
        return stand
    else: 
        return False
@stand_router.get("/stand/seller/{idseller}", status_code = status.HTTP_200_OK, response_model=List[StandResponse] | bool)
def get_stand_by_user_id(idseller: int, db: Session = Depends(get_db)):
    stands = db.query(StandModel).filter(StandModel.idseller == idseller).all()
    if(stands): 
        return stands
    else: 
        return False
@stand_router.get("/stand/category/{category}", status_code= status.HTTP_200_OK, response_model=List[StandResponse] | bool) 
def get_stand_by_category(category: int, db: Session = Depends(get_db)):
    stands = db.query(StandModel).filter(StandModel.category == category).all() 
    if(stands): 
        return stands
    else: 
        return False
@stand_router.get("/category",status_code=status.HTTP_200_OK, response_model=List[CategoryResponse] | bool)
def get_categorys(db: Session = Depends(get_db)):
    stands = db.query(CategoryModel).all()
    if (stands): 
        return stands
    else : 
        return False
@stand_router.post("/category", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def add_category(category: Catetory, db: Session= Depends(get_db)):
    new_category = CategoryModel(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    db.commit()
    return new_category
@stand_router.delete("/category", status_code= status.HTTP_200_OK, response_model= bool)
def delete_category(idcategory: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.idcategory == idcategory).first()
    if category :
        db.delete(category)
        db.commit()
        return True
    else : 
        return False   
@stand_router.get("/standsWithSellers", status_code=status.HTTP_200_OK, response_model = List[StandSellerResponse] | bool)
def get_stands(db: Session = Depends(get_db)):
    standSeller = db.query(StandModel.idstand, StandModel.name.label("stand_name"), StandModel.description, StandModel.image, StandModel.horario,
                     StandModel.phone, StandModel.idseller, StandModel.street, StandModel.no_house, StandModel.colonia, StandModel.municipio,
                     StandModel.estado, StandModel.latitud, StandModel.altitud, StandModel.category, 
                     Seller.name.label("seller_name"), Seller.lastname.label("seller_lastname"))\
              .join(Seller, StandModel.idseller == Seller.iduser).all()
    if(standSeller):
        return standSeller
    else:
        return False
@stand_router.get("/standsWithSellersByIdSeller", status_code=status.HTTP_200_OK, response_model = List[StandSellerResponse] | bool)
def get_stands(idseller:int, db: Session = Depends(get_db)):
    standSeller = db.query(StandModel.idstand, StandModel.name.label("stand_name"), StandModel.description, StandModel.image, StandModel.horario,
                     StandModel.phone, StandModel.idseller, StandModel.street, StandModel.no_house, StandModel.colonia, StandModel.municipio,
                     StandModel.estado, StandModel.latitud, StandModel.altitud, StandModel.category, 
                     Seller.name.label("seller_name"), Seller.lastname.label("seller_lastname"))\
              .join(Seller, StandModel.idseller == Seller.iduser).filter(StandModel.idseller == idseller).all()
    if(standSeller):
        return standSeller
    else:
        return False    
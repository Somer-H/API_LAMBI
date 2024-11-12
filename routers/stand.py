from fastapi import APIRouter, Depends, HTTPException,status, File, UploadFile
from sqlalchemy.orm import Session
from databasecontent.database import engine, get_db, Base
from typing import List
from datetime import datetime,timedelta
from models.stand import Stand as StandModel
from schemas.stand import StandBase, StandCreate, StandResponse,StandUpdateRequest
stand_router = APIRouter()
import json

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
@stand_router.put("/sellers/{idstand}", status_code=status.HTTP_201_CREATED, response_model=StandResponse)
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
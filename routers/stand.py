from fastapi import APIRouter, Depends, HTTPException,status, File, UploadFile
from sqlalchemy.orm import Session
from databasecontent.database import engine, get_db, Base
from typing import List
from datetime import datetime,timedelta
from models.stand import Stand as StandModel
from schemas.stand import StandBase, StandCreate, StandResponse
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

from fastapi import APIRouter, Depends, HTTPException,status, File, UploadFile
from sqlalchemy.orm import Session
from databasecontent.database import engine, get_db, Base
from typing import List
from datetime import datetime,timedelta
from models.stand import Stand as StandModel
from schemas.stand import StandBase, StandCreate, StandResponse
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
import json
stand_router = APIRouter()

@stand_router.post("/stand", status_code=status.HTTP_200_OK, response_model=StandResponse)
def create_stand(stand: StandCreate, db: Session = Depends(get_db)):
    new_stand = StandModel(**stand.dict())
    new_stand.location = json.dumps(new_stand.location)
    db.add(new_stand)
    db.commit()
    db.refresh(new_stand)
    
    return new_stand
@stand_router.get('/stand/{iduser}', status_code=status.HTTP_200_OK, response_model=List[StandResponse])
def get_all_stand(iduser: int, db: Session = Depends(get_db)):
    all_stands = db.query(StandModel).filter(StandModel.iduser == iduser).all
    return all_stands

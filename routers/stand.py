from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from databasecontent.database import engine, get_db, Base
from typing import List
from datetime import datetime,timedelta
from models.stand import Stand as StandModel
from schemas.stand import Stand, StandBase, StandCreate


stand_router = APIRouter()

@stand_router.post("/stand", response_model=Stand)
def create_stand(stand: StandCreate, db: Session = Depends(get_db)):
    stand_data = stand.dict()
    if stand.location:
        stand_data["location"] = stand.location.dict()
    
    db_stand = StandModel(**stand_data)
    db.add(db_stand)
    db.commit()
    db.refresh(db_stand)
    return db_stand
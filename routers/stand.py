from fastapi import APIRouter, Depends, HTTPException,status, File, UploadFile
from sqlalchemy.orm import Session
from databasecontent.database import engine, get_db, Base
from typing import List
from datetime import datetime,timedelta
from models.stand import Stand as StandModel
from schemas.stand import StandBase, StandCreate, StandResponse, Adress
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
import json
from sqlalchemy import text, bindparam
stand_router = APIRouter()
from sqlalchemy import text, bindparam
import json

import json

@stand_router.post("/stand", status_code=status.HTTP_200_OK, response_model=StandResponse)
def create_stand(stand: StandCreate, db: Session = Depends(get_db)):
    # Serializa los objetos location a un formato compatible con PostgreSQL
    serialized_location = [
        {
            "street": address.street,
            "no_house": address.no_house,
            "colonia": address.colonia,
            "municipio": address.municipio,
            "estado": address.estado,
            "latitud": address.latitud,
            "altitud": address.altitud
        }
        for address in stand.location
    ]

    # Convierte el objeto serializado en una cadena JSON

    # Define la consulta SQL para la inserción
    query = text("""
    INSERT INTO Stand (name, description, image, category, horario, phone, iduser, location)
    VALUES (:name, :description, :image, :category, :horario, :phone, :iduser, :location)
    """)

    # Ejecuta la consulta con los parámetros, asegurándote de que location esté correctamente serializado
    query = query.bindparams(
        bindparam("name", value=stand.name),
        bindparam("description", value=stand.description),
        bindparam("image", value=stand.image),
        bindparam("category", value=stand.category),
        bindparam("horario", value=stand.horario),
        bindparam("phone", value=stand.phone),
        bindparam("iduser", value=stand.iduser),
        bindparam("location", value=serialized_location)  # Pasa el array serializado como JSON
    )

    # Ejecuta la consulta
    result = db.execute(query)

    # Recupera el nuevo "stand" después de la inserción
    final = result.fetchone()

    # Commit de los cambios
    db.commit()

    return final
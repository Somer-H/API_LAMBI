from fastapi import APIRouter, Depends, HTTPException,status, Form,File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from databasecontent.database import get_db
from typing import List
from fastapi.security import  HTTPAuthorizationCredentials, HTTPBearer
from models.favorite import Favorite
from models.stand import Stand as StandModel, CategoryModel
from models.buyer import RateModel
from sellers.seller_models import Seller
from schemas.stand import StandResponse,StandUpdateRequest, Catetory, CategoryResponse, StandSellerResponse, StandFavoriteResponse
from schemas.favorite import FavoriteResponse
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, ClientError
stand_router = APIRouter()
import os
from dotenv import load_dotenv
load_dotenv()
bearer_scheme = HTTPBearer()
product_router = APIRouter()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_images_to_s3(image_files: List[UploadFile], bucket_name: str) -> List[str]:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=AWS_REGION_NAME
    )
    uploaded_urls = []

    for image_file in image_files:
        try:
            # Generar un nombre único para cada imagen
            unique_filename = f"{uuid.uuid4()}.{image_file.filename.split('.')[-1]}"
            
            # Subir la imagen al bucket S3
            s3_client.upload_fileobj(image_file.file, bucket_name, unique_filename)
            
            # Construir la URL de la imagen y agregarla a la lista
            image_url = f"https://{bucket_name}.s3.{AWS_REGION_NAME}.amazonaws.com/{unique_filename}"
            uploaded_urls.append(image_url)
        
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="Error with AWS credentials")
        except ClientError as e:
            # Captura el error específico de AWS S3
            raise HTTPException(status_code=500, detail=f"AWS ClientError: {str(e)}")
        except Exception as e:
            # Otros errores
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    return uploaded_urls

@stand_router.post("/protected/stand", status_code=status.HTTP_200_OK, response_model=StandResponse)
def create_stand(
    name: str = Form(...),
    description: str = Form(...),
    image: List[UploadFile] = File(...),     
    category: int = Form(...),
    street: str = Form(...),
    no_house: str = Form(...),
    colonia: str = Form(...),
    municipio: str = Form(...),
    estado: str = Form(...),
    latitud: float = Form(...),
    altitud: float = Form(...),
    horario: str = Form(...),
    phone: List[str] = Form(...),
    idseller: int = Form(...),
    send_to_house: bool = Form(...),
    db: Session = Depends(get_db), 
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        image_urls = []
        if image:
            image_urls = upload_images_to_s3(image, S3_BUCKET_NAME)
            print(f"Uploaded image URLs: {image_urls}")  # Verifica si las URLs están siendo generadas
            print(image_urls)
        if not image:
            raise HTTPException(status_code=400, detail="No image files were provided.")
        new_stand = StandModel(
            name=name,
            description=description,
            image=image_urls,  
            category=category,
            street=street,
            no_house=no_house,
            colonia=colonia,
            municipio=municipio,
            estado=estado,
            latitud=latitud,
            altitud=altitud,
            horario=horario,
            phone=phone,  
            idseller=idseller,
            send_to_house= send_to_house  
        )

        # Agregar el nuevo stand a la base de datos
        db.add(new_stand)
        db.commit()
        db.refresh(new_stand)  # Actualizar el objeto con los datos de la base de datos

        return new_stand  # Devolver el nuevo stand creado

    except HTTPException as e:
        raise e

    except Exception as e:
        print("Error durante el registro del producto:", e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
@stand_router.get('/protected/stand', status_code=status.HTTP_200_OK, response_model=List[StandResponse])
def get_all_stands(db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    all_stands = db.query(StandModel).all()
    return all_stands
@stand_router.put("/protected/stand/{idstand}", status_code=status.HTTP_201_CREATED, response_model=StandResponse)
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
    if stand_update.send_to_house is not None:
        stand.send_to_house = stand_update.send_to_house        
    if updated:
        try:
            db.commit()
            db.refresh(stand)
            return stand
        except Exception as e:
            db.rollback()
            return stand
@stand_router.delete("/protected/stand/{idstand}", status_code=status.HTTP_200_OK, response_model= bool)
def delete_stand(idstand: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
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
@stand_router.get("/protected/stand/seller/{idseller}", status_code = status.HTTP_200_OK, response_model=List[StandResponse] | bool)
def get_stand_by_user_id(idseller: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
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
@stand_router.post("/protected/category", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def add_category(category: Catetory, db: Session= Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    new_category = CategoryModel(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    db.commit()
    return new_category
@stand_router.delete("/protected/category", status_code= status.HTTP_200_OK, response_model= bool)
def delete_category(idcategory: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
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
@stand_router.get("/favorite", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(db: Session = Depends(get_db)):
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
            #.c es para acceder a la columna, ya que el .group_by me lo guarda todo como si de una tabla se tratase
        )
        .outerjoin(Favorite, StandModel.idstand == Favorite.idstand)
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .all()
    )

    if favorites:
        return favorites
    else:
        return False
@stand_router.get("/favorite/withRatingOnly", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(db: Session = Depends(get_db)):
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            rating.c.rating
            #.c es para acceder a la columna, ya que el .group_by me lo guarda todo como si de una tabla se tratase
        )
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .all()
    )

    if favorites:
        return favorites
    else:
        return False    
@stand_router.get("/protected/favorite{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(idbuyer: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
            #.c es para acceder a la columna, ya que el .group_by me lo guarda todo como si de una tabla se tratase
        )
        .outerjoin(Favorite, StandModel.idstand == Favorite.idstand)
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .filter(Favorite.iduser == idbuyer).all()
    )

    if favorites:
        return favorites
    else:
        return False    
@stand_router.get("/protected/favoriteWIthCategory/{category}/{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(category: int, idbuyer: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Subconsulta para calificaciones
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )

    # Consulta principal
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
        )
        .outerjoin(Favorite, and_(StandModel.idstand == Favorite.idstand, Favorite.iduser == idbuyer))  # Solo favoritos del idbuyer
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .filter(StandModel.category == category)  # Todos los stands de la categoría
        .all()
    )

    # Retorno de resultados
    if favorites:
        return favorites
    else:
        return False
@stand_router.get("/protected/Allfavorites/{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(idbuyer: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Subconsulta para calificaciones
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )

    # Consulta principal
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
        )
        .outerjoin(Favorite, and_(StandModel.idstand == Favorite.idstand, Favorite.iduser == idbuyer))  # Solo favoritos del idbuyer
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .all()
    )

    # Retorno de resultados
    if favorites:
        return favorites
    else:
        return False        
@stand_router.get("/favoriteByIdStand/{idbuyer}/{idstand}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(idbuyer: int, idstand: int, db: Session = Depends(get_db)):
    # Subconsulta para calificaciones
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )

    # Consulta principal
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
        )
        .outerjoin(Favorite, and_(StandModel.idstand == Favorite.idstand, Favorite.iduser == idbuyer))  # Solo favoritos del idbuyer
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .filter(StandModel.idstand == idstand)  # Todos los favoritos del stand con idstand
        .all()
    )

    # Retorno de resultados
    if favorites:
        return favorites
    else:
        return False            
@stand_router.get("/protected/favoriteWIthName/{name}/{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(name: str, idbuyer: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
        )
        .group_by(RateModel.idstand)
        .subquery()
    )
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            Favorite.iduser.label("favorite_user"),
            Favorite.status.label("favorite_status"),
            rating.c.rating
            #.c es para acceder a la columna, ya que el .group_by me lo guarda todo como si de una tabla se tratase
        )
        .outerjoin(Favorite, StandModel.idstand == Favorite.idstand)
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .filter(StandModel.name.ilike(f"%{name}%")).filter(or_(Favorite.iduser == idbuyer, Favorite.iduser==None)).all()
    )

    if favorites:
        return favorites
    else:
        return False        
@stand_router.get("/protected/standWithRating/{idstand}", status_code=status.HTTP_200_OK, response_model=StandFavoriteResponse | bool)
def get_favorites_byId(idstand: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    rating = (
        db.query(
            RateModel.idstand,
            func.avg(RateModel.stars).label("rating")
            #en la documentación viene la función avg que sirve para calcular el promedio, pues aquí me sirve
        )
        .group_by(RateModel.idstand)
        #el subquery sirve para poder mandar a llamar este query para alguna otra ocasión, no se ejecuta en el momento
        .subquery()
    )
    favorites = (
        db.query(
            StandModel.idstand,
            StandModel.name,
            StandModel.description,
            StandModel.idseller,
            StandModel.street,
            StandModel.no_house,
            StandModel.colonia,
            StandModel.municipio,
            StandModel.estado,
            StandModel.image,
            StandModel.category,
            StandModel.horario,
            StandModel.phone,
            StandModel.altitud,
            StandModel.latitud,
            rating.c.rating
            #.c es para acceder a la columna, ya que el .group_by me lo guarda todo como si de una tabla se tratase
        )
        .outerjoin(rating, StandModel.idstand == rating.c.idstand)
        .filter(StandModel.idstand == idstand).first()
    )

    if favorites:
        return favorites
    else:
        return False
    
@stand_router.get("/protected/favoritebyId/{iduser}/{idstand}", status_code=status.HTTP_200_OK, response_model= FavoriteResponse | bool)
def get_favorite_byId(iduser: int, idstand: int, db: Session= Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)): 
            favorite = db.query(Favorite).filter(Favorite.iduser == iduser).filter(Favorite.idstand == idstand).first()
            if(favorite): 
                return favorite
            else: 
                return False
@stand_router.get("/protected/stand/seller/{idseller}/{search_term}", status_code=status.HTTP_200_OK, response_model=List[StandResponse] | bool)
def get_stand_by_user_id(idseller: int, search_term: str, db: Session = Depends(get_db)):
    stands = db.query(StandModel).filter(
        StandModel.idseller == idseller,
        StandModel.name.ilike(f"%{search_term}%")
    ).all()
    
    if stands:
        return stands
    else:
        return False             
@stand_router.get("/stand/search/{search_term}", status_code=status.HTTP_200_OK, response_model=List[StandResponse] | bool)
def get_stand_by_user_id(search_term: str, db: Session = Depends(get_db)):
    stands = db.query(StandModel).filter(
        StandModel.name.ilike(f"%{search_term}%")
    ).all()
    
    if stands:
        return stands
    else:
        return False                 
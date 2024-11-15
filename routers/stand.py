from fastapi import APIRouter, Depends, HTTPException,status, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from databasecontent.database import get_db
from typing import List
from models.favorite import Favorite
from models.stand import Stand as StandModel, CategoryModel
from models.buyer import RateModel
from sellers.seller_models import Seller
from schemas.stand import StandResponse,StandUpdateRequest, Catetory, CategoryResponse, StandSellerResponse, StandFavoriteResponse
from schemas.favorite import FavoriteResponse
stand_router = APIRouter()
@stand_router.post("/stand", status_code=status.HTTP_200_OK, response_model=StandResponse)
def create_stand(
    name: str = Form(...),
    description: str = Form(...),
    image: List[str] = Form(...),     
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
    db: Session = Depends(get_db)
):
    try:
        new_stand = StandModel(
            name=name,
            description=description,
            image=image,  # Recibimos las listas directamente
            category=category,
            street=street,
            no_house=no_house,
            colonia=colonia,
            municipio=municipio,
            estado=estado,
            latitud=latitud,
            altitud=altitud,
            horario=horario,
            phone=phone,  # Recibimos las listas directamente
            idseller=idseller
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
@stand_router.get("/favoriteWIthCategory/{category}/{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(category: int, idbuyer: int, db: Session = Depends(get_db)):
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
        .filter(StandModel.category == category).filter(or_(Favorite.iduser == idbuyer, Favorite.iduser==None)).all()
    )

    if favorites:
        return favorites
    else:
        return False
@stand_router.get("/favoriteWIthName/{name}/{idbuyer}", status_code=status.HTTP_200_OK, response_model=List[StandFavoriteResponse] | bool)
def get_favorites(name: str, idbuyer: int, db: Session = Depends(get_db)):
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
@stand_router.get("/standWithRating/{idstand}", status_code=status.HTTP_200_OK, response_model=StandFavoriteResponse | bool)
def get_favorites_byId(idstand: int, db: Session = Depends(get_db)):
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
    
@stand_router.get("/favoritebyId/{iduser}/{idstand}", status_code=status.HTTP_200_OK, response_model= FavoriteResponse | bool)
def get_favorite_byId(iduser: int, idstand: int, db: Session= Depends(get_db)): 
            favorite = db.query(Favorite).filter(Favorite.iduser == iduser).filter(Favorite.idstand == idstand).first()
            if(favorite): 
                return favorite
            else: 
                return False
@stand_router.get("/stand/seller/{idseller}/{search_term}", status_code=status.HTTP_200_OK, response_model=List[StandResponse] | bool)
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
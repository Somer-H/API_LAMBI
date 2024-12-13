from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi.security import  HTTPAuthorizationCredentials, HTTPBearer
from schemas.products import Product,ProductBase,ProductCreate,ProductUpdate, CategoryProduct, CategoryProductResponse
from models.products import Product as ProductModel, CategoryBase
from datetime import datetime,timedelta
from typing import List, Optional
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, ClientError
from databasecontent.database import engine, get_db, Base
import os
from dotenv import load_dotenv
bearer_scheme = HTTPBearer()
load_dotenv()
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


@product_router.post("/protected/products/", response_model=Product)
async def create_product(name: str = Form(...),description: str = Form(...),price: float = Form(...), amount: int = Form(...), category: int = Form(...), image: Optional[List[UploadFile]] = File(...), standid:int = Form(...), db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        print(f"Received image files: {image}") 
        image_urls = []
        if image:
            image_urls = upload_images_to_s3(image, S3_BUCKET_NAME)
            print(f"Uploaded image URLs: {image_urls}")  # Verifica si las URLs están siendo generadas
            print(image_urls)
        if not image:
            raise HTTPException(status_code=400, detail="No image files were provided.")    
        # Crear el nuevo producto
        new_product = ProductModel(
            name=name,
            description=description,
            price=price,
            amount=amount,
            category=category,
            image=image_urls, 
            standid=standid
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
     
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print("Error durante el registro del producto:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
@product_router.post("/protected/categoryProduct/", response_model=CategoryProductResponse)
def add_category_product(category_product: CategoryProduct, db:Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try: 
        new_category_product = CategoryBase(**category_product.dict())
        db.add(new_category_product)
        db.commit()
        db.refresh(new_category_product)
        return new_category_product; 
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error durante la actualización del producto:", e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during update.")
@product_router.get("/protected/products/get", response_model=List[Product])
async def get_products(db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return db.query(ProductModel).all()
@product_router.get("/protected/categoryProduct/", response_model=List[CategoryProductResponse])
def get_category_products(db:Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return db.query(CategoryBase).all()
@product_router.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.put("/protected/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db),authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    product_to_update = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()
    if not product_to_update:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_update is not None:
        product_to_update.name = product_update.name
    if product_update.description is not None:
        product_to_update.description = product_update.description
    if product_update.price is not None:
        product_to_update.price = product_update.price
    if product_update.amount is not None:
        product_to_update.amount = product_update.amount
    if product_update.category is not None:
        product_to_update.category = product_update.category  
    if product_to_update.image is not None: 
        product_to_update.image = product_update.image
    db.commit()
    db.refresh(product_to_update)
    return product_to_update


@product_router.delete("/protected/products", response_model=Product)
async def delete_product(product_id: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    product_to_delete = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()
    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product_to_delete)
    db.commit()
    return product_to_delete

@product_router.get("/products/search/{search_term}", response_model=List[Product])
async def search_products(search_term: str, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.name.contains(search_term)).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found matching the search term.")
    return products

@product_router.get("/products/recent", response_model=List[Product])
async def get_recent_products(db: Session = Depends(get_db)):
    recent_products = db.query(ProductModel).order_by(ProductModel.created_at.desc()).limit(5).all()
    if not recent_products:
        raise HTTPException(status_code=404, detail="No recent products found.")
    return recent_products

@product_router.get("/products/category/{category}", response_model=List[Product])
async def get_products_by_category(category: int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.category == category).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in the specified category.")
    return products

@product_router.get("/protected/products/seller/{stand_id}", response_model=List[Product])
async def get_products_by_seller(stand_id: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    products = db.query(ProductModel).filter(ProductModel.standid == stand_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found by the specified seller.")
    return products
@product_router.get("/products/found/product/{search_term}", response_model=List[Product])
async def search_products(search_term: str, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.name.ilike(f"%{search_term}%")).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found matching the search term.")
    return products  
@product_router.get("/productsWithStandId/{standid}", response_model=List[Product])
def get_products_with_stand_id(standid: int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.standid == standid).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in the specified stand.")
    return products
@product_router.put("/protected/products/images/{product_id}", response_model=Product)
async def add_images_to_product(
    product_id: int, 
    image: Optional[List[UploadFile]] = File(None), 
    db: Session = Depends(get_db),
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    product_to_update = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()

    if not product_to_update:
        raise HTTPException(status_code=404, detail="Product not found")
    if image is not None:
        new_image_urls = upload_images_to_s3(image, S3_BUCKET_NAME)
        print(f"New image URLs: {new_image_urls}")
        product_to_update.image = product_to_update.image + new_image_urls
        print(product_to_update.image)
        db.commit()
        db.refresh(product_to_update)
        return product_to_update
    else :
        raise HTTPException(status_code=400, detail="No image provided")
    


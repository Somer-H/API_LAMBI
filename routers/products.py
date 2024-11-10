from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from schemas.products import Product,ProductBase,ProductCreate,ProductUpdate
from models.products import Product as ProductModel
from datetime import datetime,timedelta
from typing import List
import boto3
import uuid
from botocore.exceptions import NoCredentialsError
from databasecontent.database import engine, get_db, Base

product_router = APIRouter()

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = "us-east-1"
S3_BUCKET_NAME = "lambiimage"


def upload_image_to_s3(image_file: UploadFile, bucket_name: str) -> str:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )
    try:
        # Generar un nombre único para la imagen
        unique_filename = f"{uuid.uuid4()}.{image_file.filename.split('.')[-1]}"
        
        # Subir la imagen al bucket S3
        s3_client.upload_fileobj(image_file.file, bucket_name, unique_filename)
        
        # Construir la URL de la imagen
        image_url = f"https://{bucket_name}.s3.{AWS_REGION_NAME}.amazonaws.com/{unique_filename}"
        return image_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Error with AWS credentials")
    except Exception as e:
        print("Error uploading image:", e)
        raise HTTPException(status_code=500, detail="Error uploading image")




@product_router.get("/products/", response_model=List[Product])
async def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@product_router.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = ProductModel(
            name=product.name,
            description = product.description,
            price=product.price,
            amount=product.amount,
            category=product.category,
            image=product.image, 
            sellerid=product.sellerid      
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

@product_router.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_to_update = db.query(ProductModel).filter(ProductModel.idproduct == product_id).first()
    if not product_to_update:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name is not None:
        product_to_update.name = product.name
    if product.description is not None:
        product_to_update.description = product.description
    if product.price is not None:
        product_to_update.price = product.price
    if product.amount is not None:
        product_to_update.amount = product.amount
    if product.category is not None:
        product_to_update.category = product.category
    if product.image is not None:
        product_to_update.image = product.image

    db.commit()
    db.refresh(product_to_update)
    return product_to_update


@product_router.delete("/products", response_model=Product)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
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

@product_router.get("/products/category/{category_name}", response_model=List[Product])
async def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.category == category_name).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in the specified category.")
    return products

@product_router.get("/products/seller/{seller_id}", response_model=List[Product])
async def get_products_by_seller(seller_id: int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(ProductModel.sellerid == seller_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found by the specified seller.")
    return products
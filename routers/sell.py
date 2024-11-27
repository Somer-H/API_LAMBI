from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.security import  HTTPAuthorizationCredentials, HTTPBearer
from databasecontent.database import get_db
from typing import List
from models.sell import SellModel, SellProduct as SellProductModel
from schemas.sell import SellProductResponse, UpdateSell, SellProduct, SellRequest, SellResponse, SellProductResponseNow
from models.products import Product
sell_router = APIRouter()
bearer_scheme = HTTPBearer()
@sell_router.post("/protected/sell", status_code=status.HTTP_201_CREATED, response_model=SellProductResponse)
def create_sell(
    sell: SellRequest,
    db: Session = Depends(get_db),
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        all_products = db.query(Product).all()
        products_dict = {product.idproduct: product for product in all_products}
        new_sell = SellModel(
            hour=sell.hour,
            date=sell.date,
            description=sell.description,
            standid_fk=sell.standid_fk,
            idbuyer=sell.idbuyer,
            direccion_entrega= sell.direccion_entrega
        )
        db.add(new_sell)
        db.commit()  
        db.refresh(new_sell)
        inserted_sells = {"sell": new_sell, "sells": []}
        id = new_sell.idsell
        total_price = 0
        for sellProductInsert in sell.sells:
            sellProduct = SellProductModel(
                idsell=id,
                idproduct=sellProductInsert.idproduct,
                amount=sellProductInsert.amount
            )
            db.add(sellProduct)
            inserted_sells["sells"].append(sellProduct)
            product = products_dict.get(sellProductInsert.idproduct)
            if product:
                if product.amount < sellProductInsert.amount:
                    db.delete(new_sell)
                    db.commit()
                    db.rollback()
                    raise HTTPException(
                        status_code=400,
                        detail="La cantidad que intenta ingresar es mayor a la que existe"
                    )
                else:
                    total_price += product.price * sellProductInsert.amount
            else:
                db.rollback()
                db.delete(new_sell)
                db.commit()
                raise HTTPException(
                    status_code=400,
                    detail="Este producto no se encontró"
                )
        new_sell.total_price = total_price
        db.commit()
        inserted_sells["total_price"] = total_price
        for product in inserted_sells["sells"]:
            db.refresh(product)
        
        return inserted_sells
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error durante el registro del producto:", e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
@sell_router.get("/sell/products/{standid_fk}", response_model=List[SellProductResponseNow])
async def get_sell_details_by_stand(standid_fk: int, db: Session = Depends(get_db)):
    try:
        query = (
            db.query(
                SellModel.idsell,
                SellModel.date,
                SellModel.description.label("sell_description"),
                SellModel.hour,
                SellModel.idbuyer,
                SellModel.standid_fk,
                Product.category,
                Product.description.label("product_description"),
                Product.image,
                Product.name,
                Product.price,
                SellProductModel.idproduct,
                SellProductModel.amount,
                SellModel.total_price,
                SellModel.direccion_entrega
            )
            .join(SellProductModel, SellModel.idsell == SellProductModel.idsell)
            .join(Product, Product.idproduct == SellProductModel.idproduct)
            .filter(SellModel.standid_fk == standid_fk)
            .all()  
        )
        if not query:
            raise HTTPException(status_code=404, detail="No sales found for the specified stand.")
        return query
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
@sell_router.put("/protected/sell/{idsell}", status_code=status.HTTP_201_CREATED, response_model=SellResponse | bool)
def put_sell(idsell: int, sell_update: UpdateSell, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if not sell:
        raise HTTPException(status_code=404, detail="Seller not found")
    updated = False
    if sell_update.date is not None:
        sell.date = sell_update.date
        updated = True
    if sell_update.hour is not None:
        sell.hour = sell_update.hour
        updated = True
    if sell_update.description is not None:
        sell.description = sell_update.description
        updated = True    
    if sell_update.direccion_entrega is not None:
       sell.direccion_entrega = sell_update.direccion_entrega 
       updated = True  
    if updated:
        try:
            db.commit()
            db.refresh(sell)
            return sell
        except Exception as e:
            db.rollback()
            return sell
@sell_router.delete("/protected/sell/{idsell}", status_code=status.HTTP_200_OK, response_model= bool)
def delete_sell(idsell: int, db: Session = Depends(get_db),  authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if sell :
       db.delete(sell)
       db.commit()
       return True
    else :
        return False        
@sell_router.get("/protected/sell/{idsell}", status_code=status.HTTP_200_OK, response_model=SellResponse | bool)
def get_sell_byId(idsell: int, db: Session = Depends(get_db),  authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)): 
    sell = db.query(SellModel).filter(SellModel.idsell == idsell).first()
    if(sell): 
        return sell
    else: 
        return False
@sell_router.post("/protected/sellProduct", status_code = status.HTTP_201_CREATED, response_model= SellProduct)
def add_sell_product(sell: SellProduct, db: Session = Depends(get_db),  authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)): 
    try:
     new_sell = SellModel(**sell.dict())
     db.add(new_sell)
     db.commit()
     return new_sell 
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print("Error durante el registro del producto:", e) 
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
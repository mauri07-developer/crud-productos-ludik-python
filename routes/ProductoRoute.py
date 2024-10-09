from typing import Annotated, Optional,List
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from schemas.Producto import ProductoResponse,Producto
from controllers.ProductoController import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)
from database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Ruta para crear un producto
@router.post("/product/save")
def create(product: Producto, db: Session = Depends(get_db)):
    return create_product(product, db)

# Ruta para listar todos los productos
@router.get("/products/")
def read_all(db: Session = Depends(get_db)):
    return get_products(db)

# Ruta para obtener un producto específico
@router.get("/product/{id}")
def read(id: int, db: Session = Depends(get_db)):
    return get_product(id, db)

# Ruta para actualizar un producto
@router.put("/product/update/{id}", response_model=ProductoResponse)
def update(id: int, product: Producto, db: Session = Depends(get_db)):
    return update_product(id, product, db)

# Ruta para eliminar (inactivar) un producto
@router.delete("/product/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)



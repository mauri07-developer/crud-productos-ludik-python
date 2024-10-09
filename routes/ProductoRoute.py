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
@router.post("/product/save" ,description="Crea un nuevo producto")
def create(product: Producto, db: Session = Depends(get_db)):
    return create_product(product, db)

# Ruta para listar todos los productos
@router.get("/products/",description="Listar todos los productos")
def read_all(db: Session = Depends(get_db)):
    return get_products(db)

# Ruta para obtener un producto específico
@router.get("/product/{id}",description="Obtener un producto especifico")
def read(id: int, db: Session = Depends(get_db)):
    return get_product(id, db)

# Ruta para actualizar un producto
@router.put("/product/update/{id}",description="Actualizar un producto")
def update(id: int, product: Producto, db: Session = Depends(get_db)):
    return update_product(id, product, db)

# Ruta para eliminar (inactivar) un producto
@router.delete("/product/delete/{id}",description="Eliminar un producto")
def delete(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)



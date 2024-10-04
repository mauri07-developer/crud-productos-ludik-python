from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
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

@router.get("/productos")
def planes_get(
    search: str = "", page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    return get_planes(db, search, page, per_page)

@router.get("/producto")
def plan_get(plan_id: int, db: Session = Depends(get_db)):
    return get_plan(db, plan_id)


# Ruta para crear un producto
@router.post("/productos/", response_model=ProductoResponse)
def create(product: Producto, db: Session = Depends(get_db)):
    return create_product(product, db)

# Ruta para listar todos los productos
@router.get("/productos/", response_model=List[ProductoResponse])
def read_all(db: Session = Depends(get_db)):
    return get_products(db)

# Ruta para obtener un producto específico
@router.get("/productos/{id}", response_model=ProductoResponse)
def read(id: int, db: Session = Depends(get_db)):
    return get_product(id, db)

# Ruta para actualizar un producto
@router.put("/productos/{id}", response_model=ProductoResponse)
def update(id: int, product: Producto, db: Session = Depends(get_db)):
    return update_product(id, product, db)

# Ruta para eliminar (inactivar) un producto
@router.delete("/productos/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)



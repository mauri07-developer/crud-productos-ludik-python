import os
from typing import Optional
from fastapi import File, Request, Response, UploadFile,HTTPException
from models.Producto import productos
from fastapi.responses import FileResponse
# from nanoid import generate
from schemas.Producto import *
from sqlalchemy import text
from sqlalchemy.orm import Session
import math

# from utils.File import get_extension, getImage, remove_file, save_file, update_filename
# from utils.Image import get_avif_support, get_webp_support


def create_product(product: Producto, db: Session):
    new_product = productos.insert().values(
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio,
        stock=product.stock,
        estado=product.estado
    )
    db.execute(new_product)
    db.commit()
    return db.execute(productos.select().order_by(productos.c.id.desc())).first()

# Función para obtener todos los productos
def get_products(db: Session):
    return db.execute(productos.select().where(productos.c.estado == 1)).fetchall()

# Función para obtener un producto específico
def get_product(id: int, db: Session):
    product = db.execute(productos.select().where(productos.c.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# Función para actualizar un producto
def update_product(id: int, product: Producto, db: Session):
    existing_product = db.execute(productos.select().where(productos.c.id == id)).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update_query = productos.update().where(productos.c.id == id).values(
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio,
        stock=product.stock,
        estado=product.estado
    )
    db.execute(update_query)
    db.commit()
    return db.execute(productos.select().where(productos.c.id == id)).first()

# Función para eliminar (inactivar) un producto
def delete_product(id: int, db: Session):
    product = db.execute(productos.select().where(productos.c.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.execute(productos.update().where(productos.c.id == id).values(estado=0))
    db.commit()
    return {"message": "Producto eliminado con éxito"}
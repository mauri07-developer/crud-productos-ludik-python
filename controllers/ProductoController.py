import os
from typing import Optional
from fastapi import File, Request, Response, UploadFile,HTTPException
from models.Producto import productos
from fastapi.responses import FileResponse
from schemas.Producto import *
from sqlalchemy import text,and_
from sqlalchemy.orm import Session
import math


#Funcion para crear productos
def create_product(product: Producto, db: Session):
    try:
        # Creo la consulta de inserción para producto
        new_product = productos.insert().values(
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio=product.precio,
            stock=product.stock
        )

        # Ejecuto la consulta de inserción
        db.execute(new_product)
        db.commit()

        # Devuelvo la respuesta de éxito
        return {
            "message": "Se registró correctamente el producto",
            "state": True,
            "code": 200
        }
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        return {
            "message": str(e),
            "state": False,
            "code": 400  # Puedes cambiar este código según el tipo de error
        }

# Función para obtener todos los productos
def get_products(db: Session):
    # Ejecuto la consulta y obtiene los productos activos
    result = db.execute(productos.select().where(productos.c.estado == 1)).fetchall()
    
    # Mapeo una lista de productos
    products = [
        {
            "id": row.id,
            "nombre": row.nombre,
            "descripcion": row.descripcion,
            "precio": row.precio,
            "stock": row.stock,
            "estado": row.estado,
            "created_at":row.created_at,
            "updated_at":row.updated_at
        }
        for row in result
    ]
    
    return products

# Función para obtener un producto específico
def get_product(id: int, db: Session):
    result = db.execute(productos.select().where(and_(productos.c.id == id,productos.c.estado==1))).first()

    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado o se encuentra inactivo")
    
    # Construyo el objeto correspondiente al producto
    product = {
        "id": result.id,
        "nombre": result.nombre,
        "descripcion": result.descripcion,
        "precio": result.precio,
        "stock": result.stock,
        "estado": result.estado,
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }
    
    return product

# Función para actualizar un producto
def update_product(id: int, product: Producto, db: Session):
    try:
        # Verifico si el producto existe
        existing_product = db.execute(productos.select().where(and_(productos.c.id == id,productos.c.estado==1))).first()

        if not existing_product:
            return {
                "message": "Producto no encontrado o se encuentra inactivo",
                "state": False,
                "code": 404
            }

        # Creo la consulta de actualizacion
        update_query = productos.update().where(productos.c.id == id).values(
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio=product.precio,
            stock=product.stock
        )

        # Ejecuto la consulta de actualización
        db.execute(update_query)
        db.commit()

        # Obtengo el producto actualizado para devolverlo
        updated_product = db.execute(productos.select().where(productos.c.id == id)).first()

        # Mapeo la tupla a un diccionario para devolver
        producto_data = {
            "id": updated_product.id,
            "nombre": updated_product.nombre,
            "descripcion": updated_product.descripcion,
            "precio": updated_product.precio,
            "stock": updated_product.stock,
            "estado": updated_product.estado
        }

        # Devolver la respuesta de éxito
        return {
            "message": "Producto actualizado con éxito",
            "state": True,
            "code": 200,
            "producto": producto_data  
        }

    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        return {
            "message": "No se pudo actualizar el producto",
            "state": False,
            "code": 500  
        }

# Función para eliminar (inactivar) un producto
def delete_product(id: int, db: Session):

    # Buscar el producto por su id
    product = db.execute(productos.select().where(productos.c.id == id)).first()

    # Si no se encuentra el producto o esta inactivo, devolver un mensaje personalizado
    if not product:
        return {"message": "Producto no encontrado o se encuentra inactivo", "code": 404, "estado": False}

    # Actualizar el estado del producto a 0 (eliminado)
    db.execute(productos.update().where(productos.c.id == id).values(estado=0))
    db.commit()

    # Retornar el mensaje de éxito
    return {"message": "Producto eliminado con éxito", "code": 200, "estado": True}
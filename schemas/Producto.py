from pydantic import BaseModel, constr,condecimal,Field
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    nombre: constr(min_length=1, max_length=255, strip_whitespace=True)  # Cadena no vacía con longitud entre 1 y 255
    descripcion: constr(max_length=500) = None  # Descripción opcional con un máximo de 500 caracteres
    precio: condecimal(gt=0, max_digits=10)  # Decimal positivo con máximo 10 dígitos y 2 decimales
    stock: int = Field(..., gt=0)  # Entero positivo

    class Config:
        orm_mode = True

# Modelo para la respuesta
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int


    class Config:
        orm_mode = True
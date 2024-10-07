from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    estado: Optional[int] = 1

    class Config:
        orm_mode = True

# Modelo para la respuesta
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    estado: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
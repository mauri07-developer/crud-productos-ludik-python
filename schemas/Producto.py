from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    id: Optional[int]         # id puede ser opcional al crear un nuevo producto
    nombre: str
    descripcion: str
    precio: float
    stock: int
    estado: Optional[int] = 1 # Valor por defecto 1 para productos activos
    created_at: Optional[datetime]  # Opcional, ya que se generará automáticamente
    updated_at: Optional[datetime]  # Opcional, también generado automáticamente

    class Config:
        orm_mode = True  # Esto permite trabajar fácilmente con objetos ORM como SQLAlchemy
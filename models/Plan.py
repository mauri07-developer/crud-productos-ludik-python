from pydantic import BaseModel


class Producto(BaseModel):
    id: int
    nombre: str
    descripcion:str
    precio:float
    stock:int
    created_at:str
    updated_at:str
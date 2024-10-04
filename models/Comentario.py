from pydantic import BaseModel


class Comentario(BaseModel):
    comentario_nombre: str
    comentario_descripcion: str
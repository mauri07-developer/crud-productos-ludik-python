from pydantic import BaseModel


class Licencia(BaseModel):
    licencia_plan: int
    licencia_nombre: str
    licencia_descripcion: str
    licencia_precionormal: float
    licencia_preciodescuento: float
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from controllers.LicenciaController import (
    get_licencia,
    get_licencias
)
from database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/licencias")
def licencias_get(
    search: str = "", page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    return get_licencias(db, search, page, per_page)

@router.get("/licencia")
def licencia_get(licencia_id: int, db: Session = Depends(get_db)):
    return get_licencia(db, licencia_id)




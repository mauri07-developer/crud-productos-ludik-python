from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from controllers.ComentarioController import (
    get_comentario,
    get_comentarios
)
from database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/comentarios")
def comentarios_get(
    search: str = "", page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    return get_comentarios(db, search, page, per_page)

@router.get("/comentario")
def comentario_get(comentario_id: int, db: Session = Depends(get_db)):
    return get_comentario(db, comentario_id)




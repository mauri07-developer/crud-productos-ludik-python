from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from controllers.PlanController import (
    get_plan,
    get_planes
)
from database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/planes")
def planes_get(
    search: str = "", page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    return get_planes(db, search, page, per_page)

@router.get("/plan")
def plan_get(plan_id: int, db: Session = Depends(get_db)):
    return get_plan(db, plan_id)




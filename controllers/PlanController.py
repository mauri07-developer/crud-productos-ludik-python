import os
from typing import Optional
from fastapi import File, Request, Response, UploadFile
from fastapi.responses import FileResponse
# from nanoid import generate
from models.Plan import *
from sqlalchemy import text
import math

# from utils.File import get_extension, getImage, remove_file, save_file, update_filename
# from utils.Image import get_avif_support, get_webp_support


def get_planes(db, search, page, per_page):
    try:
        offset = (page - 1) * per_page

        sql_query = text(
            """
            SELECT COUNT(*) AS Filas FROM plan
            WHERE
            (
                LOWER(CONCAT(CAST(plan_id AS CHAR), plan_nombre, plan_descripcion))  LIKE LOWER( CONCAT( '%',:search,'%'))
            ) AND status=1
            """
        )

        planes = db.execute(sql_query, {"search": search}).fetchone()

        row = planes.Filas

        limit_query = (
            f" LIMIT :per_page OFFSET :offset"
            if per_page != -1 and per_page > -1
            else ""
        )

        sql_query = text(
            f"""
            SELECT p.* FROM plan p
            WHERE
            (
                LOWER(CONCAT(CAST(p.plan_id AS CHAR), p.plan_nombre, p.plan_descripcion)) LIKE LOWER( CONCAT( '%',:search,'%'))
            ) AND p.status=1
            {limit_query}
            """
        )

        planes = db.execute(
            sql_query, {"search": search, "per_page": per_page, "offset": offset}
        ).fetchall()

        planes = [
            {
                "plan_id": plan.plan_id,
                "plan_nombre": plan.plan_nombre,
                "plan_descripcion": plan.plan_descripcion,
            }
            for plan in planes
        ]

        planes = {
            "data": planes,
            "pages": math.ceil(
                row / per_page if per_page != -1 and per_page > -1 else 1
            ),
        }

        return planes

    except Exception as e:
        return {"message": str(e)}


def get_plan(db, plan_id):
    try:
        sql_query = text(
            """
            SELECT * FROM plan
            WHERE
            plan_id =:plan_id
            """
        )

        plan = db.execute(sql_query, {"plan_id": plan_id}).fetchone()

        plan_info = {
            "plan_id": plan.plan_id,
            "plan_nombre": plan.plan_nombre,
            "plan_descripcion": plan.plan_descripcion,
        }

        return plan_info

    except Exception as e:
        return {"message": str(e)}


def save_plan(
    db,
    nombre: str,
    # documento: int,
    nrodocumento: str,
    direccion: str,
    telefono: str,
    email: str,
	pais: str,
	ciudad: str,
):
    try:
        db.execute(
            text(
                """INSERT empresa (empresa_nombre, empresa_documento, empresa_nrodocumento, empresa_direccion, empresa_telefono, empresa_email, empresa_pais, empresa_ciudad) value (:emp_nombre, 2, :emp_nrodocumento, :emp_direccion, :emp_telefono, :emp_email, :emp_pais, :emp_ciudad)"""
            ),
            {
                "emp_nombre": nombre,
                # "emp_documento": documento,
                "emp_nrodocumento": nrodocumento,
                "emp_direccion": direccion,
                "emp_telefono": telefono,
                "emp_email": email,
				"emp_pais": pais,
                "emp_ciudad": ciudad,
            },
        )
        db.commit()

        return {"response": True, "message": "Registro realizado correctamente"}

    except Exception as e:
        return {"response": False, "message": str(e)}


async def update_plan(
    db,
    empresa_id,
    nombre: str,
    documento: int,
    nrodocumento: str,
    direccion: str,
    telefono: str,
    email: str,
    logo: UploadFile = File(None),
):
    empresa_folder = "empresas"
    file = ""
    ext = ""
    max_size = 1024 * 1024 * 10
    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    ]

    try:
        if logo is not None:
            ext = get_extension(logo)
            if ext not in extensions:
                raise ValueError("Extension de archivo no permitida")
            if logo.file:
                if  logo.size > max_size:
                    raise ValueError("Tamaño de archivo excede los 10MB")

        db.execute(
            text(
                """call empresa_update_sp(:empresa_id, :empresa_nombre, :empresa_documento, :empresa_nrodocumento, :empresa_url_logo, :empresa_direccion, :empresa_telefono, :empresa_email)"""
            ),
            {
                "empresa_id": empresa_id,
                "empresa_nombre": nombre,
                "empresa_documento": documento,
                "empresa_nrodocumento": nrodocumento,
                "empresa_url_logo": ext,
                "empresa_direccion": direccion,
                "empresa_telefono": telefono,
                "empresa_email": email,
            },
        )
        if logo is not None:
            file = await save_file(logo,folder=empresa_folder,filename= str(empresa_id), extensions=extensions)
            print(file)
        return {"response": True, "message": "Registro actualizado correctamente"}
    except Exception as e:
        print(f"""error: {file.get("webp_path")}""")
        remove_file(file.get("webp_path") if file else "")
        # remove_file(file.get("avif_path") if file else "")
        return {"response": False, "message": str(e)}


def delete_plan(db, empresa_id):
    try:
        db.execute(
            text("""
                UPDATE empresa
                SET
                status = 0
                WHERE
                empresa_id = :empresa_id
                """),
            {"empresa_id": empresa_id},
        )
        db.commit()

        return {"response": True, "message": "Registro eliminado correctamente"}

    except Exception as e:
        return {"response": False, "message": str(e)}

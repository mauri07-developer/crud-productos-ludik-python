from sqlalchemy import Table,Column,Float,DateTime,TIMESTAMP,func
from sqlalchemy.sql.sqltypes import Integer, String
from database.connection import meta,engine

# Definir la tabla productos
productos = Table(
    "productos",
    meta,
    Column("id", Integer, primary_key=True),        # ID del producto
    Column("nombre", String(255), nullable=False),  # Nombre del producto
    Column("descripcion", String(255), nullable=False), # Descripción del producto
    Column("precio", Float, nullable=False),        # Precio del producto (usamos Float para permitir decimales)
    Column("stock", Integer, nullable=False),       # Stock disponible del producto
    Column("estado", Integer, nullable=False,server_default="1"),           # Estado (1=activo, 0=inactivo)
    Column("created_at",TIMESTAMP, default=func.now()), # Fecha de creación
    Column("updated_at", TIMESTAMP, default=func.now(), onupdate=func.now()) # Fecha de última actualización
)

# Crear la tabla en la base de datos
meta.create_all(engine)
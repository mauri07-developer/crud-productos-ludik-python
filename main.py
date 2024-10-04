import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.PlanRoute import router as plan_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Filename", "Content-Response", "Content-Message"],
)

# Lista de carpetas para distintos tipos de imágenes
# carpetas = ["productos", "empresas", "default", "clientes"]
# print(carpetas)

# Crear las carpetas si no existen
# for carpeta in carpetas:
#     directorio = f"static/{carpeta}"
#     if not os.path.exists(directorio):
#         os.makedirs(directorio)

# app.mount("/default", StaticFiles(directory="static/default"), name="default_static")
# app.mount(
#     "/productos", StaticFiles(directory="static/productos"), name="productos_static"
# )
# app.mount("/empresas", StaticFiles(directory="static/empresas"), name="empresas_static")
# app.mount("/clientes", StaticFiles(directory="static/clientes"), name="clientes_static")


# planes
app.include_router(plan_router, tags=["Plan"])




from sqlalchemy import create_engine, Column, Integer, String,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from decouple import config


load_dotenv()

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_PORT = "3306"
DB_DATABASE = "crud-producto-python_ludik"
ENVIROMENT = os.getenv("ENVIROMENT")

if ENVIROMENT == "production":
    DB_HOST = config('DB_HOST')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_PORT = config('DB_PORT')
    DB_DATABASE = config('DB_DATABASE')
elif ENVIROMENT == "development":
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_PORT = "3306"
    DB_DATABASE = "crud-producto-python_ludik"



DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()

Base = declarative_base()

import os

DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
DB_HOST = "localhost"  
DB_PORT = "5432"
DB_NAME = "blacklist_db"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "supersecretkey"
JWT_SECRET_KEY = "static-token" 
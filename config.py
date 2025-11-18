import os

# Configuración base (compartida entre entornos)
class Config:
	# Lee SECRET_KEY del .env
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-clave-secreta' 
    
    # Lee las variables individuales de la DB
    DB_USER = os.environ.get('DATABASE_USER')
    DB_PASS = os.environ.get('DATABASE_PASSWORD')
    DB_HOST = os.environ.get('DATABASE_HOST')
    DB_NAME = os.environ.get('DATABASE_DB')

    # Construye la URL de conexión
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}' 
        if DB_USER and DB_PASS and DB_HOST and DB_NAME else None
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración específica para desarrollo
class DevelopmentConfig(Config):
    DEBUG = True
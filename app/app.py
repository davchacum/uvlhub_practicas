from flask import Flask
from app.routes import bp as tasks_blueprint
from .models import db # SQLAlchemy instance
from flask_migrate import Migrate
from config import DevelopmentConfig # Importamos la configuración
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(config_class=DevelopmentConfig): # Usa Desarrollo por defecto
    app = Flask(__name__)
    
    # 1. Aplicar la configuración
    app.config.from_object(config_class)
    
    # 2. Inicializar extensiones
    db.init_app(app)
    # Inicializar Flask-Migrate (necesita app y db)
    Migrate(app, db) 

    app.register_blueprint(tasks_blueprint)
        
    return app
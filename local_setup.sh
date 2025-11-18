#!/bin/bash

# =========================================================================
# SCRIPT DE SETUP Y LANZAMIENTO LOCAL PARA FLASK CON MARIADB
# =========================================================================

# --- 0. Asegurar la ubicación ---
# Cambia al directorio del script. Esto garantiza que encuentre .env y .venv.
cd "$(dirname "$0")"
echo "Directorio de trabajo actual: $(pwd)"

# --- 1. Variables y Rutas del Entorno Virtual ---
# Definimos las rutas a los binarios DENTRO del venv para usar rutas ABSOLUTAS.
VENV_DIR=".venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"
FLASK_BIN="$VENV_DIR/bin/flask"

# --- 2. Cargar Variables de Configuración desde .env ---
echo "--- 1. Cargando configuración desde el archivo .env ---"

if [ ! -f .env ]; then
    echo "❌ ERROR: El archivo .env no se encontró en $(pwd). ¡Crealo primero!"
    exit 1
fi

. .env

# Comprobación de carga
if [ -z "$DATABASE_DB" ]; then
    echo "❌ ERROR: Las variables de la base de datos (ej. DATABASE_DB) no se cargaron correctamente."
    exit 1
fi
echo "✅ Variables cargadas: Usuario=$DATABASE_USER, DB=$DATABASE_DB"

# --- 3. Preparar Entorno Python e Instalar Dependencias ---
echo "--- 2. Creando Entorno Virtual Python (.venv) ---"

# Crear el entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Usando el PIP ABSOLUTO del entorno virtual para la instalación
echo "--- Instalando dependencias necesarias (Flask, SQLAlchemy, PyMySQL, etc.) ---"
"$PIP_BIN" install --upgrade pip
# Lista de dependencias clave para el proyecto:
"$PIP_BIN" install flask python-dotenv flask-sqlalchemy pymysql flask-migrate

# --- 4. Generar requirements.txt ---
echo "--- 3. Generando requirements.txt a partir del entorno actual ---"
"$PIP_BIN" freeze > requirements.txt
echo "✅ requirements.txt creado con las dependencias instaladas."

# --- 5. Configuración de MariaDB (Usuario y Base de Datos) ---
echo "--- 4. Configurando usuario y base de datos en MariaDB... ---"

# Se ejecuta el comando SQL con las variables cargadas
# Esto requiere permisos de sudo para acceder al usuario 'root' de MariaDB
sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS $DATABASE_DB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DATABASE_USER'@'localhost' IDENTIFIED BY '$DATABASE_PASSWORD';
GRANT ALL PRIVILEGES ON $DATABASE_DB.* TO '$DATABASE_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "✅ Usuario '$DATABASE_USER' y base de datos '$DATABASE_DB' configurados."

# --- 6. Inicializar y Aplicar Migraciones ---
echo "--- 5. Aplicando migraciones de base de datos (Flask-Migrate)... ---"
"$FLASK_BIN" db init
"$FLASK_BIN" db migrate

# Exporta la variable FLASK_APP
export FLASK_APP=app.app:create_app

# Usando el binario de Flask del VENV para ejecutar la migración
"$FLASK_BIN" db upgrade

echo "✅ Migraciones completadas. Las tablas están listas."

# --- 7. Lanzar la Aplicación ---
echo "--- 6. Lanzando el servidor Flask en http://127.0.0.1:5000 ---"

# Usando el binario de Flask del VENV para ejecutar la aplicación
"$FLASK_BIN" run
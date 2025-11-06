import sys, os, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import create_app
from app import models

@pytest.fixture
def test_client():
    """Crea la aplicación Flask en modo testing y devuelve su cliente HTTP."""
    app = create_app()
    app.testing = True
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_tasks():
    """
    Fixture autouse (se ejecuta antes de cada test).
    Restablece el estado inicial de la lista de tareas.
    """
    models.tasks[:] = [
        {'id': 1, 'title': 'Comprar pan', 'done': False},
        {'id': 2, 'title': 'Estudiar Python', 'done': False}
    ]
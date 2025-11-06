import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


# === Configuración del navegador ===

def initialize_driver():
    """
    Inicializa un driver de Firefox con configuración compatible con sistemas snap.
    UVLHUB usa exactamente esta estructura.
    """
    options = webdriver.FirefoxOptions()

    # Directorio temporal alternativo (evita problemas con permisos en snap)
    snap_tmp = os.path.expanduser("~/snap/firefox/common/tmp")
    os.makedirs(snap_tmp, exist_ok=True)
    os.environ["TMPDIR"] = snap_tmp

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1024, 768)
    return driver


def close_driver(driver):
    """Cierra el navegador."""
    driver.quit()


# === Tests de interfaz ===


@pytest.fixture(scope="module")
def driver():
    """
    Fixture que crea y cierra automáticamente el navegador antes y después de todos los tests del módulo.
    """
    d = initialize_driver()
    yield d
    close_driver(d)


def test_add_task_via_web_form(driver):
    """
    Flujo de prueba:
    1. Abrir la aplicación en http://localhost:5000/
    2. Escribir una nueva tarea en el formulario.
    3. Pulsar el botón 'Añadir tarea'.
    4. Comprobar que la nueva tarea aparece en la lista.
    """

    # 1️ Navegar a la página principal
    driver.get("http://localhost:5000/")
    time.sleep(1)  # pequeña espera para que la página cargue

    # 2️ Buscar el campo de texto y escribir la tarea
    input_box = driver.find_element(By.NAME, "title")
    input_box.clear()
    input_box.send_keys("Tarea Selenium")

    # 3️ Enviar el formulario
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(1)  # espera breve tras el redireccionamiento

    # 4️ Verificar que la nueva tarea aparece en la lista
    page_source = driver.page_source
    assert "Tarea Selenium" in page_source, "La nueva tarea no se muestra en la lista de tareas."
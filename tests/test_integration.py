def test_get_tasks_endpoint_returns_existing_tasks(test_client):
    """
    GET /tasks debe devolver una lista JSON con las tareas iniciales.
    """
    response = test_client.get('/tasks')
    assert response.status_code == 200

    data = response.get_json()
    assert 'tasks' in data
    assert any(t['title'] == 'Comprar pan' for t in data['tasks'])


def test_create_task_endpoint_returns_201_and_json(test_client):
    """
    POST /tasks (API JSON) debe crear una nueva tarea y devolver status 201.
    """
    response = test_client.post('/tasks', json={'title': 'Nueva tarea'})
    assert response.status_code == 201

    data = response.get_json()
    assert data['title'] == 'Nueva tarea'
    assert 'id' in data and isinstance(data['id'], int)


def test_create_task_without_title_returns_400_error(test_client):
    """
    Si se intenta crear una tarea sin título, el servidor debe devolver error 400.
    """
    response = test_client.post('/tasks', json={})
    assert response.status_code == 400

    data = response.get_json()
    assert data['error'] == 'El título es necesario'


def test_add_task_html_redirects_and_renders_new_task(test_client):
    """
    POST /add_task (formulario HTML):
    - debe aceptar datos enviados por formulario,
    - redirigir a la lista de tareas,
    - y mostrar la nueva tarea en el HTML.
    """
    response = test_client.post(
        '/add_task',
        data={'title': 'Tarea desde HTML'},
        follow_redirects=True  # Sigue el redirect hasta la página final
    )

    # Comprobamos que la respuesta final es OK y contiene el título
    assert response.status_code == 200
    assert b'Tarea desde HTML' in response.data
    assert b'Gestor de Tareas' in response.data


def test_create_then_retrieve_task_from_api(test_client):
    """
    Flujo completo API:
    1. Crear una tarea con POST /tasks
    2. Recuperar todas las tareas con GET /tasks
    3. Verificar que la nueva está presente
    """
    test_client.post('/tasks', json={'title': 'Task persistente'})
    response = test_client.get('/tasks')
    data = response.get_json()

    titles = [t['title'] for t in data['tasks']]
    assert 'Task persistente' in titles
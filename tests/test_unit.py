import pytest
from app import models


def test_get_all_tasks_returns_list_of_dicts():
    """get_all_tasks debe devolver una lista de tareas con formato correcto."""
    result = models.get_all_tasks()
    assert isinstance(result, list)
    assert all(isinstance(t, dict) for t in result)
    assert any(t['title'] == 'Comprar pan' for t in result)


def test_create_task_adds_new_item_and_increments_length():
    """create_task debe añadir una nueva tarea y aumentar la longitud de la lista."""
    initial_len = len(models.tasks)
    new_task = models.create_task("Aprender testing")
    assert len(models.tasks) == initial_len + 1
    assert new_task in models.tasks
    assert new_task['title'] == "Aprender testing"


def test_create_task_increments_id_sequentially():
    """Los IDs de las nuevas tareas deben incrementarse de forma secuencial."""
    last_id = models.tasks[-1]['id']
    new_task = models.create_task("Nueva tarea")
    assert new_task['id'] == last_id + 1


def test_create_task_raises_value_error_if_title_missing():
    """Si no se pasa un título, create_task debe lanzar ValueError."""
    with pytest.raises(ValueError):
        models.create_task("")
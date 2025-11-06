tasks = [
    {'id': 1, 'title': 'Comprar pan', 'done': False},
    {'id': 2, 'title': 'Estudiar Python', 'done': False}
]

def get_all_tasks():
    """Devuelve la lista de tareas."""
    return tasks

def create_task(title):
    """Crea una nueva tarea con el título indicado."""
    if not title:
        raise ValueError("El título es necesario")
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': title,
        'done': False
    }
    tasks.append(new_task)
    return new_task
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }

# --- Funciones de Acceso a Datos ---

def get_all_tasks():
    with current_app.app_context():
        return [task.to_dict() for task in Task.query.order_by(Task.id).all()]

def create_task(title):
    if not title:
        raise ValueError("El título es necesario")
    
    with current_app.app_context():
        new_task = Task(title=title, done=False)
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_dict()
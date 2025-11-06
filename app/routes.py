from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models import get_all_tasks, create_task

bp = Blueprint('tasks', __name__)

@bp.route('/')
def task_list():
    return render_template('tasks.html', tasks=get_all_tasks())

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': get_all_tasks()})

@bp.route('/add_task', methods=['POST'])
def add_task_html():
    title = request.form.get('title')
    try:
        create_task(title)
        return redirect(url_for('tasks.task_list'))
    except ValueError as e:
        return str(e), 400

@bp.route('/tasks', methods=['POST'])
def create_task_api():
    data = request.get_json()
    title = data.get('title') if data else None
    try:
        task = create_task(title)
        return jsonify(task), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
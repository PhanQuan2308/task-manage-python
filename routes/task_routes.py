from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.task import Task

task_bp = Blueprint('task', __name__)

@task_bp.route('/', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.json
    Task.create_task(user_id, data['name'], data.get('description', ''), data['deadline'], data['priority'])
    return jsonify({"msg": "Task created successfully"}), 201

@task_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.get_user_tasks(user_id)  
    return jsonify(tasks), 200

@task_bp.route('/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.get_task_by_id_and_user(task_id, user_id) 
    if task:
        return jsonify(task), 200
    return jsonify({"msg": "Task not found"}), 404

@task_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.json
    Task.update_task(task_id, user_id, data)
    return jsonify({"msg": "Task updated successfully"}), 200


@task_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    Task.delete_task(task_id, user_id)
    return jsonify({"msg": "Task deleted successfully"}), 200

@task_bp.route('/<task_id>/toggle-completion', methods=['PUT'])
@jwt_required()
def toggle_task_completion(task_id):
    user_id = get_jwt_identity()
    new_status = Task.toggle_task_completion(task_id, user_id)
    if new_status is not None:
        return jsonify({"msg": "Task completion status updated", "completed": new_status}), 200
    return jsonify({"msg": "Task not found or not authorized"}), 404
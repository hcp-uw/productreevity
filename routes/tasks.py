from flask import Blueprint, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        user_id = request.headers.get('user_id')
        # Added ordering by created_at to show newest tasks first
        response = supabase.table('tasks') \
            .select("*") \
            .eq('user_id', user_id) \
            .order('created_at', desc=True) \
            .execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        user_id = request.headers.get('user_id')
        current_time = datetime.utcnow().isoformat()
        
        task_data = {
            'user_id': user_id,
            'title': data.get('title'),
            'description': data.get('description', ''),
            'notes': data.get('notes', ''),  # New field for notes
            'completed': False,
            'created_at': current_time,
            'updated_at': current_time
        }
        
        response = supabase.table('tasks').insert(task_data).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json
        user_id = request.headers.get('user_id')
        
        # Add updated_at timestamp to the update data
        update_data = {
            **data,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Ensure user owns this task before updating
        response = supabase.table('tasks') \
            .update(update_data) \
            .eq('id', task_id) \
            .eq('user_id', user_id) \
            .execute()
        
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        user_id = request.headers.get('user_id')
        response = supabase.table('tasks') \
            .delete() \
            .eq('id', task_id) \
            .eq('user_id', user_id) \
            .execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@tasks_bp.route('/tasks/<task_id>/toggle', methods=['POST'])
def toggle_task_completion(task_id):
    try:
        user_id = request.headers.get('user_id')
        
        # First get the current task state
        task = supabase.table('tasks') \
            .select("completed") \
            .eq('id', task_id) \
            .eq('user_id', user_id) \
            .execute()
        
        if not task.data:
            return jsonify({"status": "error", "message": "Task not found"}), 404
        
        # Toggle the completed status
        current_status = task.data[0]['completed']
        update_data = {
            'completed': not current_status,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        response = supabase.table('tasks') \
            .update(update_data) \
            .eq('id', task_id) \
            .eq('user_id', user_id) \
            .execute()
        
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
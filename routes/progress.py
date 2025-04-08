from flask import Blueprint, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

progress_bp = Blueprint('progress', __name__)
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@progress_bp.route('/focus/start', methods=['POST'])
def start_focus():
    try:
        user_id = request.headers.get('user_id')
        session_data = {
            'user_id': user_id,
            'start_time': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        response = supabase.table('focus_sessions').insert(session_data).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@progress_bp.route('/focus/end', methods=['POST'])
def end_focus():
    try:
        user_id = request.headers.get('user_id')
        session_id = request.json.get('session_id')
        duration = request.json.get('duration')  # duration in minutes

        # Update session
        session_data = {
            'end_time': datetime.utcnow().isoformat(),
            'duration': duration,
            'status': 'completed'
        }
        response = supabase.table('focus_sessions').update(session_data).eq('id', session_id).execute()

        # Update user achievements
        user_response = supabase.table('user_progress').select("*").eq('user_id', user_id).execute()
        
        if not user_response.data:
            # Create new progress record if doesn't exist
            progress_data = {
                'user_id': user_id,
                'total_focus_time': duration,
                'apples': duration // 30,
                'bronze_apples': 0,
                'silver_apples': 0,
                'gold_apples': 0
            }
            supabase.table('user_progress').insert(progress_data).execute()
        else:
            # Update existing progress
            current_progress = user_response.data[0]
            new_total_time = current_progress['total_focus_time'] + duration
            new_apples = current_progress['apples'] + (duration // 30)
            new_bronze = current_progress['bronze_apples'] + (new_apples // 10)
            new_silver = current_progress['silver_apples'] + (new_bronze // 10)
            new_gold = current_progress['gold_apples'] + (new_silver // 10)
            
            progress_data = {
                'total_focus_time': new_total_time,
                'apples': new_apples % 10,
                'bronze_apples': new_bronze % 10,
                'silver_apples': new_silver % 10,
                'gold_apples': current_progress['gold_apples'] + (new_silver // 10)
            }
            supabase.table('user_progress').update(progress_data).eq('user_id', user_id).execute()

        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@progress_bp.route('/progress', methods=['GET'])
def get_progress():
    try:
        user_id = request.headers.get('user_id')
        response = supabase.table('user_progress').select("*").eq('user_id', user_id).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
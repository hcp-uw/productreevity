from flask import Blueprint, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import os

auth_bp = Blueprint('auth', __name__)
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return jsonify({"status": "success", "data": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return jsonify({"status": "success", "data": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
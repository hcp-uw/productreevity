from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.progress import progress_bp
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(tasks_bp, url_prefix='/api')
app.register_blueprint(progress_bp, url_prefix='/api')

# Example route
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == "__main__":
    app.run(debug=True)
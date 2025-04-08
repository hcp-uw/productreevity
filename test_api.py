import requests
import json
from time import sleep

BASE_URL = 'http://localhost:5000/api'

def test_signup():
    print("\n=== Testing Signup ===")
    response = requests.post(f'{BASE_URL}/auth/signup', 
        json={'email': 'test@example.com', 'password': 'testpassword123'})
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_login():
    print("\n=== Testing Login ===")
    response = requests.post(f'{BASE_URL}/auth/login', 
        json={'email': 'test@example.com', 'password': 'testpassword123'})
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_task(user_id):
    print("\n=== Testing Create Task ===")
    response = requests.post(f'{BASE_URL}/tasks', 
        headers={'user_id': user_id},
        json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'notes': 'Some notes for the task'
        })
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_get_tasks(user_id):
    print("\n=== Testing Get Tasks ===")
    response = requests.get(f'{BASE_URL}/tasks', 
        headers={'user_id': user_id})
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_focus_session(user_id):
    print("\n=== Testing Focus Session ===")
    # Start focus session
    print("Starting focus session...")
    start_response = requests.post(f'{BASE_URL}/focus/start', 
        headers={'user_id': user_id})
    session_data = start_response.json()
    print(json.dumps(session_data, indent=2))
    
    # Simulate 1 minute of focus time
    print("Simulating 1 minute of focus time...")
    sleep(3)  # We'll just wait 3 seconds for testing
    
    # End focus session
    print("\nEnding focus session...")
    session_id = session_data['data'][0]['id']
    end_response = requests.post(f'{BASE_URL}/focus/end', 
        headers={'user_id': user_id},
        json={
            'session_id': session_id,
            'duration': 1  # 1 minute
        })
    print(json.dumps(end_response.json(), indent=2))

def test_get_progress(user_id):
    print("\n=== Testing Get Progress ===")
    response = requests.get(f'{BASE_URL}/progress', 
        headers={'user_id': user_id})
    print(json.dumps(response.json(), indent=2))
    return response.json()

def run_all_tests():
    # First signup and get user data
    signup_data = test_signup()
    
    # Then login
    login_data = test_login()
    
    # Get user ID from the response
    try:
        user_id = login_data['data']['user']['id']
        print(f"\nUsing user_id: {user_id}")
        
        # Test task operations
        task_data = test_create_task(user_id)
        test_get_tasks(user_id)
        
        # Test focus session
        test_focus_session(user_id)
        
        # Test progress
        test_get_progress(user_id)
        
    except KeyError as e:
        print(f"Error getting user_id from login response: {e}")
        print("Response data:", login_data)

if __name__ == "__main__":
    print("Starting API tests...")
    run_all_tests()
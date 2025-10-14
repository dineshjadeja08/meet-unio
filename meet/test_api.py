# API Testing Examples using Python requests

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

# 1. Register a new user
def test_signup():
    url = f"{BASE_URL}/auth/signup"
    data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "password2": "TestPass123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(url, json=data)
    print("Signup Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

# 2. Login
def test_login(email, password):
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    print("\nLogin Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

# 3. Create a meeting
def test_create_meeting(access_token):
    url = f"{BASE_URL}/meetings/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Meeting",
        "description": "This is a test meeting",
        "scheduled_at": "2025-10-15T10:00:00Z",
        "duration": 60
    }
    response = requests.post(url, json=data, headers=headers)
    print("\nCreate Meeting Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

# 4. Get user meetings
def test_get_meetings(access_token):
    url = f"{BASE_URL}/meetings/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print("\nGet Meetings Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

# 5. Send a chat message
def test_send_message(access_token, meeting_id):
    url = f"{BASE_URL}/chat/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "meeting_id": meeting_id,
        "message": "Hello from the API test!"
    }
    response = requests.post(url, json=data, headers=headers)
    print("\nSend Message Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

# 6. Health check
def test_health_check():
    url = f"{BASE_URL}/health/"
    response = requests.get(url)
    print("\nHealth Check Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    print("=" * 50)
    print("UNIO Backend API Test Suite")
    print("=" * 50)
    
    # Test health check first
    print("\n1. Testing Health Check...")
    test_health_check()
    
    # Test user registration
    print("\n2. Testing User Registration...")
    signup_response = test_signup()
    
    # Test login
    print("\n3. Testing User Login...")
    login_response = test_login("testuser@example.com", "TestPass123!")
    
    if "tokens" in login_response:
        access_token = login_response["tokens"]["access"]
        
        # Test create meeting
        print("\n4. Testing Create Meeting...")
        meeting_response = test_create_meeting(access_token)
        
        # Test get meetings
        print("\n5. Testing Get Meetings...")
        test_get_meetings(access_token)
        
        # Test send message
        if "id" in meeting_response:
            print("\n6. Testing Send Chat Message...")
            test_send_message(access_token, meeting_response["id"])
    
    print("\n" + "=" * 50)
    print("Test Suite Complete!")
    print("=" * 50)

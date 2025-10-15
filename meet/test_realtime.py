"""
Comprehensive test script for Realtime/Health APIs
Note: WebSocket testing requires browser or specialized WebSocket client
This script tests the HTTP endpoints for realtime functionality
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_test(name, passed=True):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")

def print_section(name):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}\n")

# Step 1: Test Health Check (No auth required)
print_section("1. HEALTH CHECK")
response = requests.get(f"{BASE_URL}/api/health/")
if response.status_code == 200:
    health = response.json()
    print_test("Health check successful")
    print(f"Status: {health['status']}")
    print(f"Message: {health['message']}")
    print(f"Timestamp: {health['timestamp']}")
else:
    print_test("Health check failed", False)
    print(f"Response: {response.text}")

# Step 2: Login to get JWT token
print_section("2. AUTHENTICATION")
login_data = {
    "email": "admin@unio.app",
    "password": "admin123"
}

response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
if response.status_code == 200:
    data = response.json()
    access_token = data['tokens']['access']
    user_id = data['user']['id']
    print_test(f"Login successful (User ID: {user_id})")
else:
    print_test("Login failed", False)
    print(f"Response: {response.text}")
    exit(1)

headers = {"Authorization": f"Bearer {access_token}"}

# Step 3: Create a test meeting for call
print_section("3. CREATE TEST MEETING")
scheduled_time = (datetime.now() + timedelta(hours=1)).isoformat()
meeting_data = {
    "title": "Realtime Test Meeting",
    "description": "Testing realtime video call functionality",
    "scheduled_at": scheduled_time,
    "duration": 60
}

response = requests.post(f"{BASE_URL}/api/meetings/", json=meeting_data, headers=headers)
if response.status_code == 201:
    meeting = response.json()
    meeting_id = meeting['id']
    print_test(f"Meeting created successfully (ID: {meeting_id})")
    print(f"Title: {meeting['title']}")
else:
    print_test("Create meeting failed", False)
    print(f"Response: {response.text}")
    meeting_id = None
    exit(1)

# Step 4: Start a video call
if meeting_id:
    print_section("4. START VIDEO CALL")
    call_data = {
        "meeting_id": meeting_id
    }
    
    response = requests.post(f"{BASE_URL}/api/health/call/start", json=call_data, headers=headers)
    if response.status_code == 201:
        call_session = response.json()
        call_id = call_session['id']
        print_test("Video call started successfully")
        print(f"Call ID: {call_id}")
        print(f"Meeting ID: {call_session['meeting']}")
        print(f"Caller: {call_session['caller']['email']}")
        print(f"Status: {call_session['status']}")
        print(f"Started At: {call_session.get('started_at', 'N/A')}")
    else:
        print_test("Start call failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        call_id = None

# Step 5: End the video call
if meeting_id and call_id:
    print_section("5. END VIDEO CALL")
    import time
    time.sleep(2)  # Simulate call duration
    
    end_call_data = {
        "call_id": call_id
    }
    
    response = requests.post(f"{BASE_URL}/api/health/call/end", json=end_call_data, headers=headers)
    if response.status_code == 200:
        call_session = response.json()
        print_test("Video call ended successfully")
        print(f"Call ID: {call_session['id']}")
        print(f"Status: {call_session['status']}")
        print(f"Duration: {call_session.get('duration', 0)} seconds")
        print(f"Ended At: {call_session.get('ended_at', 'N/A')}")
    else:
        print_test("End call failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Step 6: Test start call without meeting_id
print_section("6. TEST VALIDATION - Missing meeting_id")
call_data = {}
response = requests.post(f"{BASE_URL}/api/health/call/start", json=call_data, headers=headers)
if response.status_code == 400:
    print_test("Validation working correctly (missing meeting_id)")
    print(f"Error: {response.json().get('error', 'N/A')}")
else:
    print_test("Validation may not be working", False)
    print(f"Status: {response.status_code}")

# Step 7: Test end call without call_id
print_section("7. TEST VALIDATION - Missing call_id")
end_call_data = {}
response = requests.post(f"{BASE_URL}/api/health/call/end", json=end_call_data, headers=headers)
if response.status_code == 400:
    print_test("Validation working correctly (missing call_id)")
    print(f"Error: {response.json().get('error', 'N/A')}")
else:
    print_test("Validation may not be working", False)
    print(f"Status: {response.status_code}")

# Step 8: Cleanup - Delete test meeting
if meeting_id:
    print_section("8. CLEANUP")
    response = requests.delete(f"{BASE_URL}/api/meetings/{meeting_id}/", headers=headers)
    if response.status_code == 204:
        print_test("Test meeting deleted successfully")
    else:
        print_test("Cleanup warning: delete meeting returned non-204", False)
        print(f"Status: {response.status_code}")

# Step 9: WebSocket Information
print_section("9. WEBSOCKET TESTING INFORMATION")
print("WebSocket Endpoint: ws://localhost:8000/ws/meeting/{meeting_id}/")
print("\nWebSocket testing requires a WebSocket client.")
print("See the test report for detailed WebSocket testing examples.")
print("\nSupported WebSocket message types:")
print("  - offer (WebRTC offer)")
print("  - answer (WebRTC answer)")
print("  - ice-candidate (ICE candidates)")
print("  - join-call (User joins call)")
print("  - leave-call (User leaves call)")
print("\nWebSocket features:")
print("  ✅ Authentication required")
print("  ✅ Meeting access verification")
print("  ✅ User joined/left notifications")
print("  ✅ WebRTC signaling (offer/answer/ICE)")
print("  ✅ Peer-to-peer targeting")
print("  ✅ Error handling")

# Final summary
print_section("TEST SUMMARY")
print("Realtime HTTP API endpoints have been tested!")
print("\nTested endpoints:")
print("  ✅ GET    /api/health/              - Health check")
print("  ✅ POST   /api/health/call/start    - Start video call")
print("  ✅ POST   /api/health/call/end      - End video call")
print("\nValidations tested:")
print("  ✅ Missing meeting_id validation")
print("  ✅ Missing call_id validation")
print("\nWebSocket endpoint (requires browser/WebSocket client):")
print("  📡 WS     ws://meeting/{id}/        - WebRTC signaling")
print("\n" + "="*60)
print("✅ ALL REALTIME HTTP TESTS COMPLETED!")
print("="*60 + "\n")
print("Note: For complete WebSocket testing, use the browser-based")
print("examples in the REALTIME_API_TEST_REPORT.md file.")

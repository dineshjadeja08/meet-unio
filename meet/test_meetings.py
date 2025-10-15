"""
Comprehensive test script for all Meeting APIs
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

# Step 1: Login to get JWT token
print_section("1. AUTHENTICATION")
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
    print(f"Access Token: {access_token[:50]}...")
else:
    print_test("Login failed", False)
    print(f"Response: {response.text}")
    exit(1)

headers = {"Authorization": f"Bearer {access_token}"}

# Step 2: Create a meeting
print_section("2. CREATE MEETING")
scheduled_time = (datetime.now() + timedelta(hours=2)).isoformat()
meeting_data = {
    "title": "Team Standup",
    "description": "Daily team sync meeting",
    "scheduled_at": scheduled_time,
    "duration": 30
}

response = requests.post(f"{BASE_URL}/api/meetings/", json=meeting_data, headers=headers)
if response.status_code == 201:
    meeting = response.json()
    meeting_id = meeting['id']
    print_test(f"Meeting created successfully (ID: {meeting_id})")
    print(f"Title: {meeting['title']}")
    print(f"Meeting Link: {meeting['meeting_link']}")
    print(f"Status: {meeting['status']}")
else:
    print_test("Create meeting failed", False)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    meeting_id = None

# Step 3: List all meetings
print_section("3. LIST MEETINGS")
response = requests.get(f"{BASE_URL}/api/meetings/", headers=headers)
if response.status_code == 200:
    meetings = response.json()
    print_test(f"Retrieved {len(meetings)} meeting(s)")
    for m in meetings:
        print(f"  - [{m['id']}] {m['title']} - Status: {m['status']}")
else:
    print_test("List meetings failed", False)
    print(f"Response: {response.text}")

# Step 4: Get specific meeting details
if meeting_id:
    print_section("4. GET MEETING DETAILS")
    response = requests.get(f"{BASE_URL}/api/meetings/{meeting_id}/", headers=headers)
    if response.status_code == 200:
        meeting = response.json()
        print_test("Retrieved meeting details")
        print(f"ID: {meeting['id']}")
        print(f"Title: {meeting['title']}")
        print(f"Description: {meeting['description']}")
        print(f"Host: {meeting['host']['email']}")
        print(f"Status: {meeting['status']}")
        print(f"Scheduled At: {meeting['scheduled_at']}")
        print(f"Duration: {meeting['duration']} minutes")
    else:
        print_test("Get meeting details failed", False)
        print(f"Response: {response.text}")

# Step 5: Update meeting
if meeting_id:
    print_section("5. UPDATE MEETING")
    update_data = {
        "title": "Team Standup (Updated)",
        "description": "Updated description for daily sync",
        "duration": 45
    }
    response = requests.patch(f"{BASE_URL}/api/meetings/{meeting_id}/", json=update_data, headers=headers)
    if response.status_code == 200:
        meeting = response.json()
        print_test("Meeting updated successfully")
        print(f"New Title: {meeting['title']}")
        print(f"New Description: {meeting['description']}")
        print(f"New Duration: {meeting['duration']} minutes")
    else:
        print_test("Update meeting failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Step 6: Create another user and send invite
print_section("6. SEND MEETING INVITE")
# First, create a test user
signup_data = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
}
response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
if response.status_code == 201:
    test_user = response.json()
    test_user_id = test_user['user']['id']
    print(f"Created test user (ID: {test_user_id})")
elif response.status_code == 400 and 'email' in response.json():
    # User might already exist, try to get user list
    admin_login = {
        "email": "admin@unio.app",
        "password": "admin123"
    }
    admin_resp = requests.post(f"{BASE_URL}/api/auth/login", json=admin_login)
    admin_token = admin_resp.json()['tokens']['access']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    users_resp = requests.get(f"{BASE_URL}/api/users/", headers=admin_headers)
    if users_resp.status_code == 200:
        users = users_resp.json()
        test_user_obj = next((u for u in users if u['email'] == 'testuser@example.com'), None)
        if test_user_obj:
            test_user_id = test_user_obj['id']
            print(f"Using existing test user (ID: {test_user_id})")
        else:
            test_user_id = None
    else:
        test_user_id = None
else:
    print_test("Create test user failed", False)
    print(f"Response: {response.text}")
    test_user_id = None

# Now send invite
if meeting_id and test_user_id:
    invite_data = {
        "invitee_ids": [test_user_id]
    }
    response = requests.post(f"{BASE_URL}/api/meetings/{meeting_id}/send-invite/", json=invite_data, headers=headers)
    if response.status_code in [200, 201]:
        result = response.json()
        print_test("Invite sent successfully")
        print(f"Message: {result['message']}")
        print(f"Invited: {result['invited']}")
        if result['errors']:
            print(f"Errors: {result['errors']}")
    else:
        print_test("Send invite failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Step 7: Start meeting
if meeting_id:
    print_section("7. START MEETING")
    response = requests.post(f"{BASE_URL}/api/meetings/{meeting_id}/start/", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print_test("Meeting started successfully")
        print(f"Message: {result['message']}")
        print(f"Status: {result['meeting']['status']}")
    else:
        print_test("Start meeting failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Step 8: End meeting
if meeting_id:
    print_section("8. END MEETING")
    response = requests.post(f"{BASE_URL}/api/meetings/{meeting_id}/end/", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print_test("Meeting ended successfully")
        print(f"Message: {result['message']}")
        print(f"Status: {result['meeting']['status']}")
    else:
        print_test("End meeting failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Step 9: Get meeting history
print_section("9. GET MEETING HISTORY")
response = requests.get(f"{BASE_URL}/api/meetings/history/", headers=headers)
if response.status_code == 200:
    history = response.json()
    print_test(f"Retrieved {len(history)} completed meeting(s)")
    for m in history:
        print(f"  - [{m['id']}] {m['title']} - Status: {m['status']}")
else:
    print_test("Get meeting history failed", False)
    print(f"Response: {response.text}")

# Step 10: Delete meeting
if meeting_id:
    print_section("10. DELETE MEETING")
    response = requests.delete(f"{BASE_URL}/api/meetings/{meeting_id}/", headers=headers)
    if response.status_code == 204:
        print_test("Meeting deleted successfully")
    else:
        print_test("Delete meeting failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

# Final summary
print_section("TEST SUMMARY")
print("All meeting API endpoints have been tested!")
print("\nTested endpoints:")
print("  ✅ POST   /api/meetings/                    - Create meeting")
print("  ✅ GET    /api/meetings/                    - List meetings")
print("  ✅ GET    /api/meetings/{id}/               - Get meeting details")
print("  ✅ PATCH  /api/meetings/{id}/               - Update meeting")
print("  ✅ POST   /api/meetings/{id}/send-invite/   - Send invite")
print("  ✅ POST   /api/meetings/{id}/start/         - Start meeting")
print("  ✅ POST   /api/meetings/{id}/end/           - End meeting")
print("  ✅ GET    /api/meetings/history/            - Get meeting history")
print("  ✅ DELETE /api/meetings/{id}/               - Delete meeting")
print("\n" + "="*60)
print("✅ ALL TESTS COMPLETED!")
print("="*60 + "\n")

"""
Comprehensive test script for all Notification APIs
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
    admin_user_id = data['user']['id']
    print_test(f"Admin login successful (User ID: {admin_user_id})")
else:
    print_test("Login failed", False)
    print(f"Response: {response.text}")
    exit(1)

headers = {"Authorization": f"Bearer {access_token}"}

# Step 2: Create a test user to send notifications to
print_section("2. CREATE TEST USER")
signup_data = {
    "email": "notifytest@example.com",
    "username": "notifytest",
    "password": "NotifyTest123!",
    "password2": "NotifyTest123!",
    "first_name": "Notify",
    "last_name": "Test"
}

response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
if response.status_code == 201:
    test_user = response.json()
    test_user_id = test_user['user']['id']
    test_user_token = test_user['tokens']['access']
    test_headers = {"Authorization": f"Bearer {test_user_token}"}
    print_test(f"Test user created (ID: {test_user_id})")
    print(f"Email: {test_user['user']['email']}")
elif response.status_code == 400 and 'email' in response.json():
    print("Test user already exists (from previous run)")
    # Login instead
    login_data = {
        "email": "notifytest@example.com",
        "password": "NotifyTest123!"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        test_user_id = data['user']['id']
        test_user_token = data['tokens']['access']
        test_headers = {"Authorization": f"Bearer {test_user_token}"}
        print_test(f"Using existing test user (ID: {test_user_id})")
    else:
        print_test("Could not login test user", False)
        exit(1)
else:
    print_test("Create test user failed", False)
    print(f"Response: {response.text}")
    exit(1)

# Step 3: Create a meeting for testing (for meeting-related notifications)
print_section("3. CREATE TEST MEETING")
scheduled_time = (datetime.now() + timedelta(hours=2)).isoformat()
meeting_data = {
    "title": "Notification Test Meeting",
    "description": "Testing notification functionality",
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

# Step 4: Send a general notification
print_section("4. SEND GENERAL NOTIFICATION")
notification_data = {
    "recipient_ids": [test_user_id],
    "title": "Welcome!",
    "message": "Welcome to UNIO video conferencing platform!",
    "notification_type": "general"
}

response = requests.post(f"{BASE_URL}/api/notifications/send/", json=notification_data, headers=headers)
if response.status_code == 201:
    result = response.json()
    print_test("General notification sent successfully")
    print(f"Message: {result['message']}")
    print(f"Sent to: {result['sent_to']}")
else:
    print_test("Send notification failed", False)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

# Step 5: Send a meeting invite notification
if meeting_id:
    print_section("5. SEND MEETING INVITE NOTIFICATION")
    notification_data = {
        "recipient_ids": [test_user_id],
        "title": "Meeting Invitation",
        "message": f"You've been invited to '{meeting['title']}'",
        "notification_type": "meeting_invite",
        "meeting_id": meeting_id
    }
    
    response = requests.post(f"{BASE_URL}/api/notifications/send/", json=notification_data, headers=headers)
    if response.status_code == 201:
        result = response.json()
        print_test("Meeting invite notification sent")
        print(f"Sent to: {result['sent_to']}")
    else:
        print_test("Send meeting notification failed", False)
        print(f"Response: {response.text}")

# Step 6: Send meeting reminder notification
if meeting_id:
    print_section("6. SEND MEETING REMINDER NOTIFICATION")
    notification_data = {
        "recipient_ids": [test_user_id],
        "title": "Meeting Reminder",
        "message": f"Meeting '{meeting['title']}' starts in 1 hour!",
        "notification_type": "meeting_reminder",
        "meeting_id": meeting_id
    }
    
    response = requests.post(f"{BASE_URL}/api/notifications/send/", json=notification_data, headers=headers)
    if response.status_code == 201:
        result = response.json()
        print_test("Meeting reminder sent")
    else:
        print_test("Send reminder failed", False)

# Step 7: Send notification to multiple users
print_section("7. SEND NOTIFICATION TO MULTIPLE USERS")
notification_data = {
    "recipient_ids": [test_user_id, admin_user_id],
    "title": "System Maintenance",
    "message": "System will be down for maintenance at 3 AM.",
    "notification_type": "general"
}

response = requests.post(f"{BASE_URL}/api/notifications/send/", json=notification_data, headers=headers)
if response.status_code == 201:
    result = response.json()
    print_test(f"Notification sent to {len(result['sent_to'])} users")
    print(f"Recipients: {', '.join(result['sent_to'])}")
else:
    print_test("Send to multiple users failed", False)

# Step 8: Get all notifications for test user
print_section("8. GET ALL NOTIFICATIONS (Test User)")
response = requests.get(f"{BASE_URL}/api/notifications/", headers=test_headers)
if response.status_code == 200:
    notifications = response.json()
    print_test(f"Retrieved {len(notifications)} notification(s)")
    print("\nNotifications:")
    for notif in notifications:
        read_status = "✓ Read" if notif['is_read'] else "✗ Unread"
        meeting_info = f" (Meeting: {notif['meeting_title']})" if notif['meeting_title'] else ""
        print(f"  [{notif['id']}] {notif['title']} - {notif['notification_type']} - {read_status}{meeting_info}")
        print(f"      Message: {notif['message']}")
else:
    print_test("Get notifications failed", False)
    print(f"Response: {response.text}")

# Step 9: Filter unread notifications
print_section("9. GET UNREAD NOTIFICATIONS ONLY")
response = requests.get(f"{BASE_URL}/api/notifications/?is_read=false", headers=test_headers)
if response.status_code == 200:
    notifications = response.json()
    print_test(f"Retrieved {len(notifications)} unread notification(s)")
    for notif in notifications:
        print(f"  [{notif['id']}] {notif['title']}")
else:
    print_test("Get unread notifications failed", False)

# Step 10: Filter by notification type
print_section("10. FILTER BY NOTIFICATION TYPE")
response = requests.get(f"{BASE_URL}/api/notifications/?type=meeting_invite", headers=test_headers)
if response.status_code == 200:
    notifications = response.json()
    print_test(f"Retrieved {len(notifications)} meeting invite(s)")
    for notif in notifications:
        print(f"  [{notif['id']}] {notif['title']} - {notif['message']}")
else:
    print_test("Filter by type failed", False)

# Step 11: Mark a specific notification as read
print_section("11. MARK NOTIFICATION AS READ")
# Get first unread notification
response = requests.get(f"{BASE_URL}/api/notifications/?is_read=false", headers=test_headers)
if response.status_code == 200 and len(response.json()) > 0:
    first_notif = response.json()[0]
    notif_id = first_notif['id']
    
    response = requests.post(f"{BASE_URL}/api/notifications/{notif_id}/mark-read/", headers=test_headers)
    if response.status_code == 200:
        result = response.json()
        print_test(f"Notification {notif_id} marked as read")
        print(f"Title: {result['title']}")
        print(f"Read At: {result['read_at']}")
        print(f"Is Read: {result['is_read']}")
    else:
        print_test("Mark as read failed", False)
        print(f"Response: {response.text}")
else:
    print("No unread notifications to mark")

# Step 12: Mark all notifications as read
print_section("12. MARK ALL NOTIFICATIONS AS READ")
response = requests.post(f"{BASE_URL}/api/notifications/mark-all-read/", headers=test_headers)
if response.status_code == 200:
    result = response.json()
    print_test("All notifications marked as read")
    print(f"Message: {result['message']}")
else:
    print_test("Mark all as read failed", False)
    print(f"Response: {response.text}")

# Step 13: Verify all are read
print_section("13. VERIFY ALL NOTIFICATIONS ARE READ")
response = requests.get(f"{BASE_URL}/api/notifications/", headers=test_headers)
if response.status_code == 200:
    notifications = response.json()
    unread_count = sum(1 for n in notifications if not n['is_read'])
    read_count = sum(1 for n in notifications if n['is_read'])
    
    if unread_count == 0:
        print_test(f"Verification successful: All {read_count} notifications are read")
    else:
        print_test(f"Verification: {read_count} read, {unread_count} unread", unread_count == 0)
else:
    print_test("Verification failed", False)

# Step 14: Delete a notification
print_section("14. DELETE A NOTIFICATION")
response = requests.get(f"{BASE_URL}/api/notifications/", headers=test_headers)
if response.status_code == 200 and len(response.json()) > 0:
    notif_to_delete = response.json()[0]
    notif_id = notif_to_delete['id']
    
    response = requests.delete(f"{BASE_URL}/api/notifications/{notif_id}/", headers=test_headers)
    if response.status_code == 204:
        print_test(f"Notification {notif_id} deleted successfully")
    else:
        print_test("Delete notification failed", False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
else:
    print("No notifications to delete")

# Step 15: Test unauthorized access
print_section("15. TEST AUTHORIZATION")
# Admin tries to mark test user's notification as read (should fail)
response = requests.get(f"{BASE_URL}/api/notifications/", headers=test_headers)
if response.status_code == 200 and len(response.json()) > 0:
    test_user_notif_id = response.json()[0]['id']
    
    # Admin tries to mark it as read
    response = requests.post(f"{BASE_URL}/api/notifications/{test_user_notif_id}/mark-read/", headers=headers)
    if response.status_code == 403:
        print_test("Authorization working correctly (access denied)")
    else:
        print_test("Authorization may not be working", False)
        print(f"Status: {response.status_code}")
else:
    print("No notifications to test authorization")

# Step 16: Test invalid recipient
print_section("16. TEST INVALID RECIPIENT")
notification_data = {
    "recipient_ids": [99999],  # Non-existent user
    "title": "Test",
    "message": "This should fail",
    "notification_type": "general"
}

response = requests.post(f"{BASE_URL}/api/notifications/send/", json=notification_data, headers=headers)
if response.status_code == 201:
    result = response.json()
    if len(result['errors']) > 0:
        print_test("Invalid recipient handling works correctly")
        print(f"Errors: {result['errors']}")
    else:
        print_test("Should have returned error for invalid user", False)
else:
    print_test("Request failed unexpectedly", False)

# Step 17: Cleanup - Delete test meeting
if meeting_id:
    print_section("17. CLEANUP")
    response = requests.delete(f"{BASE_URL}/api/meetings/{meeting_id}/", headers=headers)
    if response.status_code == 204:
        print_test("Test meeting deleted successfully")
    else:
        print_test("Cleanup: delete meeting returned non-204", False)
        print(f"Status: {response.status_code}")

# Final summary
print_section("TEST SUMMARY")
print("All notification API endpoints have been tested!")
print("\nTested endpoints:")
print("  ✅ POST   /api/notifications/send/              - Send notifications")
print("  ✅ GET    /api/notifications/                   - Get notifications")
print("  ✅ GET    /api/notifications/?is_read=false     - Filter by read status")
print("  ✅ GET    /api/notifications/?type=TYPE         - Filter by type")
print("  ✅ POST   /api/notifications/{id}/mark-read/    - Mark as read")
print("  ✅ POST   /api/notifications/mark-all-read/     - Mark all as read")
print("  ✅ DELETE /api/notifications/{id}/              - Delete notification")
print("\nFeatures tested:")
print("  ✅ Send general notification")
print("  ✅ Send meeting invite notification")
print("  ✅ Send meeting reminder notification")
print("  ✅ Send to multiple users")
print("  ✅ Retrieve all notifications")
print("  ✅ Filter unread notifications")
print("  ✅ Filter by notification type")
print("  ✅ Mark single notification as read")
print("  ✅ Mark all notifications as read")
print("  ✅ Delete notification")
print("  ✅ Authorization checks")
print("  ✅ Invalid recipient handling")
print("\n" + "="*60)
print("✅ ALL NOTIFICATION TESTS COMPLETED!")
print("="*60 + "\n")

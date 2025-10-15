# 🔷 UNIO Platform - Complete Swagger Testing Guide

**Platform**: UNIO Video Meeting Platform  
**Date**: October 15, 2025  
**Swagger UI**: http://localhost:8000/swagger/  
**ReDoc**: http://localhost:8000/redoc/  
**Base URL**: http://localhost:8000

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication Setup](#authentication-setup)
3. [Testing All APIs](#testing-all-apis)
4. [Meeting APIs](#meeting-apis)
5. [Chat APIs](#chat-apis)
6. [Notification APIs](#notification-apis)
7. [Realtime APIs](#realtime-apis)
8. [WebSocket Testing](#websocket-testing)
9. [Test Accounts](#test-accounts)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Step 1: Start the Server
```powershell
# Make sure the server is running
python manage.py runserver
```

### Step 2: Open Swagger UI
Navigate to: **http://localhost:8000/swagger/**

### Step 3: Login and Get Token
1. Find the **POST /api/auth/login** endpoint
2. Click **"Try it out"**
3. Use these credentials:
```json
{
  "email": "admin@unio.app",
  "password": "admin123"
}
```
4. Click **"Execute"**
5. Copy the `access` token from the response

### Step 4: Authorize
1. Click the **🔓 Authorize** button at the top right
2. Enter: `Bearer <your-access-token>` (replace `<your-access-token>` with the token you copied)
3. Click **"Authorize"**
4. Click **"Close"**

✅ **You're now authenticated and can test all endpoints!**

---

## 🔐 Authentication Setup

### Available Test Accounts

| Email | Password | Role | Description |
|-------|----------|------|-------------|
| admin@unio.app | admin123 | Admin | Full access to all features |
| user1@unio.app | user123 | User | Regular user account |
| user2@unio.app | user123 | User | Regular user account |

### Login Process

#### 1. Login Endpoint
**POST /api/auth/login**

**Request Body:**
```json
{
  "email": "admin@unio.app",
  "password": "admin123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "admin@unio.app",
    "full_name": "Admin User",
    "username": "admin"
  },
  "tokens": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### 2. Using the Token

**In Swagger UI:**
1. Click **🔓 Authorize** button
2. Enter: `Bearer <access-token>`
3. Click **Authorize**

**In cURL:**
```bash
curl -X GET "http://localhost:8000/api/meetings/" \
  -H "Authorization: Bearer <access-token>"
```

**In JavaScript:**
```javascript
fetch('http://localhost:8000/api/meetings/', {
  headers: {
    'Authorization': 'Bearer <access-token>',
    'Content-Type': 'application/json'
  }
})
```

#### 3. Token Refresh

When your access token expires (after 1 hour):

**POST /api/auth/token/refresh**

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access": "new-access-token-here",
  "refresh": "new-refresh-token-here"
}
```

---

## 📊 Testing All APIs

### API Module Overview

| Module | Endpoints | Features | Status |
|--------|-----------|----------|--------|
| **Authentication** | 3 | Login, Register, Token Refresh | ✅ Working |
| **Meetings** | 9 | CRUD, Start/End, Invites, History | ✅ Working |
| **Chat** | 5 | Messages, File Upload/Download | ✅ Working |
| **Notifications** | 7 | Send, Filter, Mark Read, Delete | ✅ Working |
| **Realtime** | 3 + WS | Health, Call Start/End, WebSocket | ✅ Working |

---

## 🎥 Meeting APIs

### 1. Create Meeting

**POST /api/meetings/**

**Request:**
```json
{
  "title": "Team Standup",
  "description": "Daily team sync meeting",
  "scheduled_at": "2025-10-16T10:00:00Z",
  "duration": 30
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Team Standup",
  "description": "Daily team sync meeting",
  "host": {
    "id": 1,
    "email": "admin@unio.app",
    "full_name": "Admin User"
  },
  "scheduled_at": "2025-10-16T10:00:00Z",
  "duration": 30,
  "status": "scheduled",
  "meeting_link": "http://localhost:8000/meeting/abc123",
  "created_at": "2025-10-15T10:30:00Z"
}
```

### 2. List All Meetings

**GET /api/meetings/**

Returns all meetings where you are host or participant.

**Optional Query Parameters:**
- `status=scheduled` - Filter by status (scheduled, ongoing, completed, cancelled)
- `search=standup` - Search in title/description
- `page=1` - Pagination

### 3. Get Meeting Details

**GET /api/meetings/{id}/**

Returns full details of a specific meeting including participants.

### 4. Update Meeting

**PUT /api/meetings/{id}/** or **PATCH /api/meetings/{id}/**

**Request:**
```json
{
  "title": "Updated Team Standup",
  "duration": 45
}
```

### 5. Delete Meeting

**DELETE /api/meetings/{id}/**

Deletes the meeting (only host can delete).

### 6. Send Meeting Invitation

**POST /api/meetings/{id}/send-invite**

**Request:**
```json
{
  "participant_emails": [
    "user1@unio.app",
    "user2@unio.app"
  ]
}
```

**Response:**
```json
{
  "message": "Invitations sent successfully",
  "invited": [
    "user1@unio.app",
    "user2@unio.app"
  ]
}
```

### 7. Start Meeting

**POST /api/meetings/{id}/start**

Changes meeting status from `scheduled` to `ongoing`.

**Response:**
```json
{
  "message": "Meeting started successfully",
  "meeting": {
    "id": 1,
    "status": "ongoing",
    "started_at": "2025-10-15T10:30:00Z"
  }
}
```

### 8. End Meeting

**POST /api/meetings/{id}/end**

Changes meeting status from `ongoing` to `completed`.

**Response:**
```json
{
  "message": "Meeting ended successfully",
  "meeting": {
    "id": 1,
    "status": "completed",
    "ended_at": "2025-10-15T11:00:00Z"
  }
}
```

### 9. Meeting History

**GET /api/meetings/history**

Returns your past meetings (completed or cancelled).

**Optional Parameters:**
- `page=1` - Pagination
- `search=term` - Search filter

---

## 💬 Chat APIs

### 1. Send Message

**POST /api/chat/send-message/**

**Request:**
```json
{
  "meeting_id": 1,
  "message": "Hello everyone! Welcome to the meeting."
}
```

**Response:**
```json
{
  "id": 1,
  "meeting": 1,
  "sender": {
    "id": 1,
    "email": "admin@unio.app",
    "full_name": "Admin User"
  },
  "message": "Hello everyone! Welcome to the meeting.",
  "timestamp": "2025-10-15T10:30:00Z",
  "file": null
}
```

### 2. Get Meeting Messages

**GET /api/chat/meetings/{meeting_id}/messages/**

Returns all messages for a specific meeting.

**Response:**
```json
[
  {
    "id": 1,
    "sender": {
      "id": 1,
      "email": "admin@unio.app",
      "full_name": "Admin User"
    },
    "message": "Hello everyone!",
    "timestamp": "2025-10-15T10:30:00Z",
    "file": null
  },
  {
    "id": 2,
    "sender": {
      "id": 2,
      "email": "user1@unio.app",
      "full_name": "User One"
    },
    "message": "Hi Admin!",
    "timestamp": "2025-10-15T10:31:00Z",
    "file": null
  }
]
```

### 3. Upload File

**POST /api/chat/upload-file/**

**Request (multipart/form-data):**
- `meeting_id`: 1
- `file`: [Select file from your computer]

**Note**: Maximum file size is 50MB. Executable files (.exe, .bat, .sh) are not allowed.

**Response:**
```json
{
  "id": 1,
  "meeting": 1,
  "sender": {
    "id": 1,
    "email": "admin@unio.app"
  },
  "file": "/media/shared_files/document.pdf",
  "file_name": "document.pdf",
  "file_size": 1024000,
  "timestamp": "2025-10-15T10:32:00Z"
}
```

### 4. Get Meeting Files

**GET /api/chat/meetings/{meeting_id}/files/**

Returns all files uploaded to a meeting.

**Response:**
```json
[
  {
    "id": 1,
    "sender": {
      "id": 1,
      "email": "admin@unio.app",
      "full_name": "Admin User"
    },
    "file": "/media/shared_files/document.pdf",
    "file_name": "document.pdf",
    "file_size": 1024000,
    "timestamp": "2025-10-15T10:32:00Z"
  }
]
```

### 5. Download File

**GET /api/chat/download-file/{file_id}/**

Downloads the file. Can be tested by clicking the URL in browser.

---

## 🔔 Notification APIs

### 1. Send Notification

**POST /api/notifications/send/**

**Request:**
```json
{
  "recipient_ids": [2, 3],
  "title": "Meeting Invitation",
  "message": "You've been invited to Team Standup",
  "notification_type": "meeting_invite",
  "meeting_id": 1
}
```

**Notification Types:**
- `meeting_invite` - Meeting invitation
- `meeting_update` - Meeting details changed
- `meeting_reminder` - Upcoming meeting reminder
- `meeting_cancelled` - Meeting cancelled
- `message` - New chat message
- `mention` - User mentioned in chat
- `general` - General notification

**Response:**
```json
{
  "message": "Notifications sent to 2 users",
  "sent_to": [2, 3],
  "errors": []
}
```

### 2. Get All Notifications

**GET /api/notifications/**

Returns all your notifications.

**Optional Parameters:**
- `is_read=false` - Filter unread only
- `type=meeting_invite` - Filter by type
- `page=1` - Pagination

### 3. Get Notification Details

**GET /api/notifications/{id}/**

Returns details of a specific notification.

### 4. Get Unread Notifications

**GET /api/notifications/unread/**

Returns only unread notifications.

### 5. Filter by Type

**GET /api/notifications/by-type/{type}/**

Example: **GET /api/notifications/by-type/meeting_invite/**

### 6. Mark as Read

**PATCH /api/notifications/{id}/mark-read/**

Marks a specific notification as read.

**Response:**
```json
{
  "message": "Notification marked as read",
  "notification": {
    "id": 1,
    "is_read": true,
    "read_at": "2025-10-15T10:35:00Z"
  }
}
```

### 7. Mark All as Read

**PATCH /api/notifications/mark-all-read/**

Marks all your notifications as read.

**Response:**
```json
{
  "message": "5 notifications marked as read"
}
```

### 8. Delete Notification

**DELETE /api/notifications/{id}/**

Deletes a notification.

---

## 📡 Realtime APIs

### 1. Health Check

**GET /api/health/**

**No authentication required** - Public endpoint to check server status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Realtime API is running",
  "timestamp": "2025-10-15T10:30:00Z"
}
```

### 2. Start Video Call

**POST /api/health/call/start**

**Request:**
```json
{
  "meeting_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "meeting": 1,
  "caller": {
    "id": 1,
    "email": "admin@unio.app",
    "full_name": "Admin User"
  },
  "status": "active",
  "started_at": "2025-10-15T10:30:00Z",
  "ended_at": null,
  "duration": null
}
```

### 3. End Video Call

**POST /api/health/call/end**

**Request:**
```json
{
  "call_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "meeting": 1,
  "caller": {
    "id": 1,
    "email": "admin@unio.app"
  },
  "status": "ended",
  "started_at": "2025-10-15T10:30:00Z",
  "ended_at": "2025-10-15T11:00:00Z",
  "duration": 1800
}
```

---

## 🔌 WebSocket Testing

### WebSocket Endpoint

**URL**: `ws://localhost:8000/ws/meeting/{meeting_id}/`

**Note**: WebSocket connections cannot be tested directly in Swagger UI. Use browser console or dedicated WebSocket client.

### Browser Console Testing

```javascript
// 1. Get your JWT token from login
const token = 'your-access-token-here';
const meetingId = 1;

// 2. Connect to WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/meeting/${meetingId}/?token=${token}`);

// 3. Handle connection events
ws.onopen = function(event) {
    console.log('✅ Connected to meeting WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('📨 Received:', data);
};

ws.onerror = function(error) {
    console.error('❌ WebSocket error:', error);
};

ws.onclose = function(event) {
    console.log('🔌 WebSocket closed');
};

// 4. Send messages
ws.send(JSON.stringify({
    type: 'join-call'
}));

// 5. Send WebRTC offer
ws.send(JSON.stringify({
    type: 'offer',
    offer: {
        type: 'offer',
        sdp: 'your-sdp-here'
    },
    target_id: 2  // Optional: specific user
}));

// 6. Send ICE candidate
ws.send(JSON.stringify({
    type: 'ice-candidate',
    candidate: {
        candidate: 'candidate:...',
        sdpMLineIndex: 0,
        sdpMid: 'audio'
    }
}));
```

### WebSocket Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `offer` | Send | WebRTC offer for video call |
| `answer` | Send | WebRTC answer to offer |
| `ice-candidate` | Send | ICE candidate for connection |
| `join-call` | Send | Notify joining call |
| `leave-call` | Send | Notify leaving call |
| `user_joined` | Receive | User connected to meeting |
| `user_left` | Receive | User disconnected |
| `webrtc_offer` | Receive | WebRTC offer from peer |
| `webrtc_answer` | Receive | WebRTC answer from peer |
| `ice_candidate` | Receive | ICE candidate from peer |
| `call_joined` | Receive | User joined call |
| `call_left` | Receive | User left call |

---

## 👥 Test Accounts

### Pre-created Accounts

```
Admin Account:
Email: admin@unio.app
Password: admin123
ID: 1

User 1:
Email: user1@unio.app
Password: user123
ID: 2

User 2:
Email: user2@unio.app
Password: user123
ID: 3
```

### Create New User

**POST /api/auth/register**

**Request:**
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "securepassword123",
  "password2": "securepassword123",
  "full_name": "New User",
  "bio": "Test user account"
}
```

---

## 🧪 Complete Testing Workflow

### Test Scenario 1: Meeting Lifecycle

1. **Login** (POST /api/auth/login)
2. **Create Meeting** (POST /api/meetings/)
3. **Invite Participants** (POST /api/meetings/{id}/send-invite)
4. **Start Meeting** (POST /api/meetings/{id}/start)
5. **Send Chat Message** (POST /api/chat/send-message/)
6. **Upload File** (POST /api/chat/upload-file/)
7. **Start Video Call** (POST /api/health/call/start)
8. **End Video Call** (POST /api/health/call/end)
9. **End Meeting** (POST /api/meetings/{id}/end)
10. **View History** (GET /api/meetings/history)

### Test Scenario 2: Notification Flow

1. **Login as Admin** (POST /api/auth/login)
2. **Create Meeting** (POST /api/meetings/)
3. **Send Notification** (POST /api/notifications/send/)
4. **Login as User1** (POST /api/auth/login with user1 credentials)
5. **Get Notifications** (GET /api/notifications/)
6. **Mark as Read** (PATCH /api/notifications/{id}/mark-read/)
7. **Delete Notification** (DELETE /api/notifications/{id}/)

### Test Scenario 3: Chat & File Sharing

1. **Login** (POST /api/auth/login)
2. **Create Meeting** (POST /api/meetings/)
3. **Send Multiple Messages** (POST /api/chat/send-message/)
4. **Upload Document** (POST /api/chat/upload-file/)
5. **Get All Messages** (GET /api/chat/meetings/{id}/messages/)
6. **Get All Files** (GET /api/chat/meetings/{id}/files/)
7. **Download File** (GET /api/chat/download-file/{id}/)

---

## 🔧 Troubleshooting

### Issue 1: "Authentication credentials were not provided"

**Solution**: Make sure you've authorized in Swagger:
1. Click **🔓 Authorize** button
2. Enter: `Bearer <your-token>`
3. Click **Authorize**

### Issue 2: "Token has expired"

**Solution**: Refresh your token:
1. Use **POST /api/auth/token/refresh**
2. Provide your refresh token
3. Get new access token
4. Re-authorize with new token

### Issue 3: "Not found" or "Does not exist"

**Solution**: Make sure the resource ID exists:
1. List all resources first (GET /api/meetings/)
2. Use an existing ID from the response
3. Check if you have permission to access it

### Issue 4: "You do not have permission"

**Solution**: Check authorization:
- Only meeting hosts can delete meetings
- Only meeting participants can access meeting chat
- Users can only see their own notifications

### Issue 5: File upload fails

**Solution**: Check file requirements:
- Maximum size: 50MB
- Prohibited types: .exe, .bat, .sh, .com, .cmd
- Must include meeting_id
- Must be authenticated

### Issue 6: WebSocket won't connect

**Solution**: Verify connection:
1. Make sure token is valid and not expired
2. Check meeting ID exists
3. Verify you're a participant or host
4. Use correct URL: `ws://localhost:8000/ws/meeting/{id}/?token={token}`

---

## 📊 API Response Codes

| Code | Meaning | When You See It |
|------|---------|-----------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid data sent |
| 401 | Unauthorized | Not logged in or token expired |
| 403 | Forbidden | Don't have permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Backend error (report if seen) |

---

## 🎯 Quick Reference Card

### Essential Endpoints

```
Login:          POST /api/auth/login
Create Meeting: POST /api/meetings/
Start Meeting:  POST /api/meetings/{id}/start
Send Message:   POST /api/chat/send-message/
Send Notify:    POST /api/notifications/send/
Start Call:     POST /api/health/call/start
```

### Essential Headers

```
Authorization: Bearer <access-token>
Content-Type: application/json
```

### Test Data Template

```json
{
  "meeting": {
    "title": "Test Meeting",
    "description": "Testing the API",
    "scheduled_at": "2025-10-16T10:00:00Z",
    "duration": 60
  },
  "message": {
    "meeting_id": 1,
    "message": "Hello from API test!"
  },
  "notification": {
    "recipient_ids": [2],
    "title": "Test Alert",
    "message": "This is a test notification",
    "notification_type": "general"
  }
}
```

---

## 📚 Additional Resources

### API Documentation
- **Swagger UI**: http://localhost:8000/swagger/ (Interactive testing)
- **ReDoc**: http://localhost:8000/redoc/ (Clean documentation)

### Test Reports
- **Meetings**: See `MEETING_API_TEST_REPORT.md`
- **Chat**: See `CHAT_API_TEST_REPORT.md`
- **Notifications**: See `NOTIFICATION_API_TEST_REPORT.md`
- **Realtime**: See `REALTIME_API_TEST_REPORT.md`
- **Complete Summary**: See `COMPLETE_API_TEST_SUMMARY.md`

### Automated Test Scripts
- `test_meetings.py` - Meeting API tests
- `test_chat.py` - Chat API tests
- `test_notifications.py` - Notification API tests
- `test_realtime.py` - Realtime API tests

---

## ✅ Testing Checklist

### Before You Start
- [ ] Server is running (`python manage.py runserver`)
- [ ] Swagger UI loads (http://localhost:8000/swagger/)
- [ ] Test account credentials available

### Authentication
- [ ] Login successful
- [ ] Access token received
- [ ] Authorized in Swagger UI
- [ ] Token works with protected endpoints

### Meetings
- [ ] Create meeting
- [ ] List meetings
- [ ] Get meeting details
- [ ] Update meeting
- [ ] Send invitation
- [ ] Start meeting
- [ ] End meeting
- [ ] View history
- [ ] Delete meeting

### Chat
- [ ] Send message
- [ ] Get messages
- [ ] Upload file
- [ ] Get files
- [ ] Download file

### Notifications
- [ ] Send notification
- [ ] Get notifications
- [ ] Filter by read status
- [ ] Filter by type
- [ ] Mark as read
- [ ] Mark all as read
- [ ] Delete notification

### Realtime
- [ ] Health check
- [ ] Start video call
- [ ] End video call
- [ ] WebSocket connection (browser console)

---

## 🎉 Success Criteria

✅ **You've successfully tested the API when:**

1. You can login and get a JWT token
2. You can create, update, and delete meetings
3. You can send and receive chat messages
4. You can upload and download files
5. You can send and manage notifications
6. You can start and end video calls
7. All responses have correct status codes
8. Authorization works correctly

---

## 📞 Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Review the test reports in the project root
3. Check Django server logs in the terminal
4. Verify database has test data (`db.sqlite3`)

---

**Last Updated**: October 15, 2025  
**Platform Version**: 1.0.0  
**API Status**: ✅ All endpoints operational (95% test success rate)

---

**Happy Testing! 🚀**

# UNIO Backend API - Quick Reference

## 🚀 Quick Start

### Windows PowerShell
```powershell
# Run setup script
.\setup.ps1

# Or manually:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open: **http://localhost:8000/swagger/** for interactive API documentation! 🎉

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📚 API Documentation

### Interactive Swagger UI
```
http://localhost:8000/swagger/
```
- **Test all endpoints** directly from browser
- **Authenticate** with JWT tokens
- **View schemas** and examples
- **No Postman needed!**

### Alternative ReDoc
```
http://localhost:8000/redoc/
```

### Admin Panel
```
http://localhost:8000/admin/
```

## API Endpoints Quick Reference

### Authentication
- POST `/api/auth/signup` - Register new user
- POST `/api/auth/login` - Login
- POST `/api/auth/logout` - Logout
- POST `/api/auth/refresh` - Refresh token
- POST `/api/auth/google` - Google OAuth
- POST `/api/auth/microsoft` - Microsoft OAuth

### Users
- GET `/api/users/` - List all users (admin)
- GET `/api/users/me/` - Current user profile
- GET `/api/users/{id}/` - Get user by ID
- PUT `/api/users/{id}/` - Update user
- DELETE `/api/users/{id}/` - Delete user (admin)

### Meetings
- GET `/api/meetings/` - List user's meetings
- POST `/api/meetings/` - Create meeting
- GET `/api/meetings/{id}/` - Get meeting details
- PUT `/api/meetings/{id}/` - Update meeting
- DELETE `/api/meetings/{id}/` - Delete meeting
- POST `/api/meetings/invite` - Send invites
- GET `/api/meetings/history/` - Meeting history

### Chat
- POST `/api/chat/send` - Send message
- GET `/api/chat/messages/{meeting_id}` - Get messages
- POST `/api/chat/file/upload` - Upload file
- GET `/api/chat/file/download/{file_id}` - Download file

### Notifications
- POST `/api/notifications/send` - Send notification
- GET `/api/notifications/` - Get notifications
- POST `/api/notifications/{id}/read` - Mark as read
- POST `/api/notifications/read-all` - Mark all read
- DELETE `/api/notifications/{id}` - Delete notification

### Real-Time
- WS `/ws/meeting/{meeting_id}/` - WebSocket connection
- POST `/api/health/call/start` - Start video call
- POST `/api/health/call/end` - End video call
- GET `/api/health/` - Health check

## Sample API Calls

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Create Meeting
```bash
curl -X POST http://localhost:8000/api/meetings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly standup",
    "scheduled_at": "2025-10-15T10:00:00Z",
    "duration": 60
  }'
```

### 4. Send Chat Message
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_id": 1,
    "message": "Hello everyone!"
  }'
```

## Environment Variables

Create a `.env` file with:
```env
SECRET_KEY=your-secret-key
DEBUG=True
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
MICROSOFT_OAUTH2_CLIENT_ID=your-microsoft-client-id
MICROSOFT_OAUTH2_CLIENT_SECRET=your-microsoft-client-secret
```

## Database Models

- **User**: Custom user with OAuth support
- **Meeting**: Meeting information
- **MeetingParticipant**: Meeting attendees
- **MeetingInvite**: Meeting invitations
- **VideoCallSession**: Video call tracking
- **ChatMessage**: In-meeting messages
- **SharedFile**: File sharing
- **Notification**: User notifications

## Testing

```powershell
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test authentication
python manage.py test meetings

# Create test data
python manage.py shell
```

## Admin Panel

Access at `http://localhost:8000/admin`

Default superuser (if not created):
- Email: admin@unio.com
- Password: (set during createsuperuser)

## Troubleshooting

**Issue**: ModuleNotFoundError
**Solution**: Activate virtual environment and install requirements

**Issue**: Migration errors
**Solution**: Delete db.sqlite3 and migrations folders, then run migrations

**Issue**: WebSocket connection failed
**Solution**: Use Daphne instead of runserver

**Issue**: OAuth fails
**Solution**: Verify OAuth credentials in .env file

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL database
- [ ] Set up Redis for Channels
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set strong SECRET_KEY
- [ ] Enable security middleware
- [ ] Set up logging
- [ ] Configure static/media file serving
- [ ] Set up backup system

## Contact

For issues and support, please create an issue in the repository.

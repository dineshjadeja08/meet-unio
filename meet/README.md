# UNIO App - Backend API

A comprehensive Django backend API for the UNIO video conferencing application with JWT authentication, OAuth support, WebSocket-based real-time communication, and meeting management features.

## Features

### 1. Authentication & Authorization
- User registration and login
- JWT token-based authentication
- Google OAuth2.0 integration
- Microsoft OAuth2.0 integration
- Token refresh mechanism
- Secure logout with token blacklisting

### 2. User Management
- User CRUD operations
- Profile management
- Role-based access control (Admin/User)
- Profile picture upload

### 3. Meeting Management
- Create, read, update, and delete meetings
- Schedule meetings with date/time
- Meeting invitations
- Meeting history tracking
- Meeting status management (scheduled, ongoing, completed, cancelled)

### 4. Real-Time Communication
- WebSocket support for WebRTC signaling
- 1:1 video call support
- Start/end call sessions
- Call duration tracking

### 5. Chat & File Sharing
- In-meeting text chat
- File upload/download during meetings
- File size and type validation
- Secure file access control

### 6. Notifications
- Push notifications for meeting invites
- Meeting reminders
- Real-time notification delivery
- Mark notifications as read/unread

### 7. Security Features
- HTTPS ready
- JWT authentication
- CORS configuration
- File upload validation
- Permission-based access control

### 8. Interactive API Documentation (Swagger UI)
- **Auto-generated API documentation**
- **Interactive testing interface**
- **Try endpoints directly from browser**
- **Authentication testing with JWT**
- **Request/Response examples**
- **OpenAPI 3.0 specification**

## API Documentation

### Swagger UI (Interactive)
Access the interactive API documentation at:
```
http://localhost:8000/swagger/
```
or
```
http://localhost:8000/
```

### ReDoc (Alternative UI)
```
http://localhost:8000/redoc/
```

**Features:**
- Browse all API endpoints
- Test endpoints directly
- View request/response schemas
- Authenticate with JWT tokens
- Download OpenAPI specification

📖 **See [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) for detailed Swagger usage instructions**

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd c:\Users\RDJ\Desktop\meet
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # OAuth Configuration
   GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
   GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
   MICROSOFT_OAUTH2_CLIENT_ID=your-microsoft-client-id
   MICROSOFT_OAUTH2_CLIENT_SECRET=your-microsoft-client-secret
   
   # Database (if using PostgreSQL)
   # DATABASE_URL=postgresql://user:password@localhost:5432/unio_db
   ```

5. **Run database migrations**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```powershell
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```powershell
   python manage.py runserver
   ```

9. **Run with Daphne (for WebSocket support)**
   ```powershell
   daphne -b 0.0.0.0 -p 8000 unio_backend.asgi:application
   ```

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/signup` | POST | Create a new user account |
| `/auth/login` | POST | Authenticate user and return JWT token |
| `/auth/logout` | POST | Logout user and invalidate token |
| `/auth/refresh` | POST | Refresh expired JWT token |
| `/auth/google` | POST | Login using Google OAuth2.0 |
| `/auth/microsoft` | POST | Login using Microsoft OAuth2.0 |

### User Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/` | GET | Get list of all users (admin only) |
| `/users/{id}/` | GET | Get user details by ID |
| `/users/` | POST | Create a new user (admin only) |
| `/users/{id}/` | PUT/PATCH | Update user profile |
| `/users/{id}/` | DELETE | Delete a user (admin only) |
| `/users/me/` | GET | Get current user profile |

### Meeting Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/meetings/` | GET | Get all meetings for logged-in user |
| `/meetings/` | POST | Create a new meeting |
| `/meetings/{id}/` | GET | Get meeting details |
| `/meetings/{id}/` | PUT/PATCH | Update meeting details |
| `/meetings/{id}/` | DELETE | Delete a meeting |
| `/meetings/invite` | POST | Send meeting invites |
| `/meetings/history/` | GET | Get meeting history |

### Real-Time Communication

| Endpoint | Type | Description |
|----------|------|-------------|
| `/ws/meeting/{meeting_id}/` | WebSocket | WebRTC signaling |
| `/health/call/start` | POST | Start a video call |
| `/health/call/end` | POST | End a video call |
| `/health/` | GET | Health check endpoint |

### Chat & File Sharing Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat/send` | POST | Send a message in meeting |
| `/chat/messages/{meeting_id}` | GET | Get all messages for meeting |
| `/chat/file/upload` | POST | Upload a file |
| `/chat/file/download/{file_id}` | GET | Download a shared file |

### Notifications Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/notifications/send` | POST | Send notifications |
| `/notifications/` | GET | Fetch user notifications |
| `/notifications/{id}/read` | POST | Mark notification as read |
| `/notifications/read-all` | POST | Mark all as read |
| `/notifications/{id}` | DELETE | Delete a notification |

## Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Request/Response Examples

### 1. User Registration
**Request:**
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Create Meeting
**Request:**
```http
POST /api/meetings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Team Standup",
  "description": "Daily team standup meeting",
  "scheduled_at": "2025-10-15T10:00:00Z",
  "duration": 30
}
```

**Response:**
```json
{
  "id": 1,
  "meeting_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Team Standup",
  "description": "Daily team standup meeting",
  "host": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe"
  },
  "scheduled_at": "2025-10-15T10:00:00Z",
  "duration": 30,
  "status": "scheduled",
  "meeting_link": "https://unio.app/meeting/550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-10-14T12:00:00Z"
}
```

### 3. WebSocket Connection (JavaScript Example)
```javascript
const meetingId = '550e8400-e29b-41d4-a716-446655440000';
const ws = new WebSocket(`ws://localhost:8000/ws/meeting/${meetingId}/`);

ws.onopen = () => {
  console.log('Connected to meeting');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
  
  // Handle different message types
  if (data.type === 'offer') {
    // Handle WebRTC offer
  } else if (data.type === 'answer') {
    // Handle WebRTC answer
  } else if (data.type === 'ice-candidate') {
    // Handle ICE candidate
  }
};

// Send WebRTC offer
ws.send(JSON.stringify({
  type: 'offer',
  offer: rtcPeerConnection.localDescription
}));
```

## Database Schema

The application uses Django ORM with the following main models:
- **User**: Custom user model with OAuth support
- **Meeting**: Meeting information and scheduling
- **MeetingParticipant**: Many-to-many relationship for meeting attendees
- **MeetingInvite**: Meeting invitation tracking
- **VideoCallSession**: Video call session management
- **ChatMessage**: In-meeting chat messages
- **SharedFile**: File sharing during meetings
- **Notification**: User notification system

## Project Structure

```
meet/
├── authentication/          # Authentication & OAuth
├── users/                   # User management
├── meetings/                # Meeting management
├── realtime/               # WebSocket & video calls
├── chat/                   # Chat & file sharing
├── notifications/          # Notification system
├── unio_backend/           # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Production Deployment

### Security Checklist
1. Set `DEBUG = False` in production
2. Use strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Enable HTTPS (`SECURE_SSL_REDIRECT = True`)
5. Set secure cookie flags
6. Use PostgreSQL instead of SQLite
7. Configure Redis for Channels layer
8. Set up proper CORS policies
9. Use environment variables for sensitive data
10. Enable security middleware

### Production Settings
```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'unio_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Use Redis for Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

## Testing

Run tests with:
```powershell
python manage.py test
```

## Admin Panel

Access the Django admin panel at:
```
http://localhost:8000/admin
```

Use your superuser credentials to manage:
- Users
- Meetings
- Chat messages
- Notifications
- Video call sessions

## Troubleshooting

### Common Issues

1. **Import errors for channels**
   - Make sure Django Channels is installed: `pip install channels`

2. **Database migration errors**
   - Delete migrations and db.sqlite3, then run migrations again

3. **WebSocket connection issues**
   - Ensure Daphne is running instead of the default Django server
   - Check CORS settings

4. **OAuth authentication fails**
   - Verify OAuth client IDs and secrets in .env file
   - Check OAuth redirect URIs in Google/Microsoft console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.

## Version

Current Version: 1.0.0
Django Version: 4.2.7
Python Version: 3.9+

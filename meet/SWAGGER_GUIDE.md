# Swagger UI - API Documentation

## Accessing Swagger UI

After starting your Django server, you can access the interactive API documentation at:

### Swagger UI (Interactive)
```
http://localhost:8000/swagger/
```
or simply:
```
http://localhost:8000/
```

### ReDoc (Alternative UI)
```
http://localhost:8000/redoc/
```

### OpenAPI Schema (JSON)
```
http://localhost:8000/swagger.json
```

### OpenAPI Schema (YAML)
```
http://localhost:8000/swagger.yaml
```

## What is Swagger UI?

Swagger UI provides:
- **Interactive API documentation** - Test endpoints directly from your browser
- **Request/Response examples** - See what data to send and expect
- **Authentication testing** - Authorize with JWT tokens and test protected endpoints
- **Schema exploration** - Browse all available endpoints and models

## How to Use Swagger UI

### 1. View Available Endpoints
- Open `http://localhost:8000/swagger/`
- Browse all API endpoints organized by categories:
  - Authentication
  - Users
  - Meetings
  - Chat
  - Notifications
  - Real-Time

### 2. Test Public Endpoints (No Auth Required)

**Example: User Registration**
1. Locate the `POST /api/auth/signup` endpoint
2. Click on it to expand
3. Click "Try it out"
4. Edit the request body:
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User"
}
```
5. Click "Execute"
6. View the response below

### 3. Authenticate for Protected Endpoints

**Step 1: Login to get JWT token**
1. Find `POST /api/auth/login`
2. Click "Try it out"
3. Enter credentials:
```json
{
  "email": "test@example.com",
  "password": "SecurePass123!"
}
```
4. Click "Execute"
5. **Copy the `access` token** from the response

**Step 2: Authorize Swagger**
1. Click the **"Authorize"** button at the top right (🔓)
2. In the dialog, enter: `Bearer <your_access_token>`
   - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. Click "Authorize"
4. Click "Close"

**Step 3: Test Protected Endpoints**
- Now all authenticated endpoints will automatically include your token
- Try `GET /api/users/me/` to get your profile
- Try `POST /api/meetings/` to create a meeting

### 4. Create and Test a Meeting

1. Make sure you're authenticated (see step 3)
2. Find `POST /api/meetings/`
3. Click "Try it out"
4. Enter meeting data:
```json
{
  "title": "Team Standup",
  "description": "Daily standup meeting",
  "scheduled_at": "2025-10-15T10:00:00Z",
  "duration": 30
}
```
5. Click "Execute"
6. Copy the `meeting_id` from the response
7. Use this ID to test other meeting endpoints

### 5. Test File Upload

1. Find `POST /api/chat/file/upload`
2. Click "Try it out"
3. Enter `meeting_id` in the form
4. Click "Choose File" and select a file
5. Click "Execute"

## Swagger UI Features

### 1. Models/Schemas
- Click on "Models" at the bottom to see all data structures
- View required fields, data types, and validation rules

### 2. Response Examples
- Each endpoint shows example responses
- Success responses (200, 201)
- Error responses (400, 401, 403, 404)

### 3. Request Body Schema
- See exactly what fields are required
- View data types and formats
- See validation constraints

### 4. Filter and Search
- Use the search box to find specific endpoints
- Filter by tags (Authentication, Users, Meetings, etc.)

## Common Workflows

### Workflow 1: User Registration and First Meeting

```
1. POST /api/auth/signup → Get tokens
2. Authorize with access token
3. POST /api/meetings/ → Create meeting
4. POST /api/meetings/invite → Invite users
5. GET /api/meetings/ → View your meetings
```

### Workflow 2: Join Meeting and Chat

```
1. POST /api/auth/login → Get tokens
2. Authorize with access token
3. GET /api/meetings/{id} → Get meeting details
4. POST /api/chat/send → Send a message
5. GET /api/chat/messages/{meeting_id} → View messages
```

### Workflow 3: File Sharing

```
1. Authenticate
2. POST /api/chat/file/upload → Upload file
3. GET /api/chat/file/download/{file_id} → Download file
```

## Tips and Tricks

### 1. Save Your Token
- After logging in, save your access token
- Tokens expire after 1 hour (configurable)
- Use refresh token to get a new access token

### 2. Test Error Scenarios
- Try invalid data to see error responses
- Test without authentication to see 401 errors
- Test with wrong user to see 403 permission errors

### 3. Use Request Body Examples
- Click on request body examples to auto-fill
- Modify as needed for your test case

### 4. Copy cURL Commands
- Each endpoint shows a cURL command
- Copy and use in terminal if needed

### 5. Download OpenAPI Spec
- Download `swagger.json` or `swagger.yaml`
- Import into Postman, Insomnia, or other tools
- Share with frontend developers

## Customization

The Swagger configuration is in `unio_backend/urls.py`:

```python
schema_view = get_schema_view(
    openapi.Info(
        title="UNIO Backend API",
        default_version='v1',
        description="Your API description",
        contact=openapi.Contact(email="support@unio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

## Enhanced Documentation

To add more detailed documentation to specific endpoints, use decorators in views:

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description="Detailed description of what this endpoint does",
    request_body=YourSerializer,
    responses={
        200: openapi.Response(
            description="Success response",
            examples={
                "application/json": {
                    "key": "value"
                }
            }
        ),
        400: "Bad Request"
    },
    tags=['YourTag']
)
@api_view(['POST'])
def your_view(request):
    pass
```

## Troubleshooting

### Issue: Swagger UI not loading
**Solution**: 
- Make sure `drf-yasg` is in INSTALLED_APPS
- Run migrations: `python manage.py migrate`
- Restart server

### Issue: Endpoints not showing
**Solution**:
- Check URL patterns in `urls.py`
- Verify apps are in INSTALLED_APPS
- Clear browser cache

### Issue: Authentication not working
**Solution**:
- Click "Authorize" button
- Enter: `Bearer <token>` (with space after Bearer)
- Make sure token is valid (not expired)

### Issue: 403 Forbidden on authenticated endpoints
**Solution**:
- Check user permissions
- Verify user is authenticated
- Some endpoints require admin access

## Production Considerations

### Disable in Production (Optional)
If you want to hide Swagger in production, modify `urls.py`:

```python
from django.conf import settings

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    ]
```

### Secure Swagger
For production with Swagger enabled:

```python
from rest_framework.permissions import IsAdminUser

schema_view = get_schema_view(
    # ... other settings ...
    permission_classes=(IsAdminUser,),  # Only admins can view
)
```

## Alternative: ReDoc

ReDoc provides a different, more documentation-focused UI:
- Visit: `http://localhost:8000/redoc/`
- Better for reading documentation
- Not interactive (can't test endpoints)
- Better for mobile viewing

## Exporting Documentation

### Export as JSON
```bash
curl http://localhost:8000/swagger.json > api-docs.json
```

### Export as YAML
```bash
curl http://localhost:8000/swagger.yaml > api-docs.yaml
```

### Generate HTML Documentation
Use tools like:
- `swagger-codegen` to generate static HTML
- `redoc-cli` to generate standalone HTML from OpenAPI spec

## Integration with Frontend

Frontend developers can:
1. Download the OpenAPI spec (swagger.json)
2. Use code generators to create API clients
3. Auto-generate TypeScript/JavaScript types
4. Generate API documentation for their apps

### Generate TypeScript Client
```bash
npm install @openapitools/openapi-generator-cli -g
openapi-generator-cli generate -i http://localhost:8000/swagger.json -g typescript-axios -o ./api-client
```

## Resources

- **drf-yasg Documentation**: https://drf-yasg.readthedocs.io/
- **Swagger/OpenAPI Spec**: https://swagger.io/specification/
- **ReDoc**: https://github.com/Redocly/redoc

---

**Quick Links:**
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- API Root: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/

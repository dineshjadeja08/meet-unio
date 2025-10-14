# ✅ UNIO Backend Server - Quick Start

## ✨ Your Swagger UI is Ready!

The backend server is now configured with **Swagger UI** for interactive API testing!

## 🚀 Start the Server

### Option 1: Using PowerShell (Recommended for Testing)
```powershell
cd c:\Users\RDJ\Desktop\meet
$env:DJANGO_SETTINGS_MODULE = 'unio_backend.settings'
python manage.py runserver
```

### Option 2: One-line Command
```powershell
cd c:\Users\RDJ\Desktop\meet; $env:DJANGO_SETTINGS_MODULE = 'unio_backend.settings'; python manage.py runserver
```

## 🌐 Access Your API

Once the server is running, open your browser:

### Swagger UI (Interactive API Documentation)
```
http://localhost:8000/swagger/
```
or
```
http://localhost:8000/
```

### ReDoc (Alternative Documentation)
```
http://localhost:8000/redoc/
```

### Admin Panel
```
http://localhost:8000/admin/
```

## 📝 Note About Environment Variable

**Important**: The environment variable `DJANGO_SETTINGS_MODULE` was previously set to `unio_meet.settings` which caused errors. 

It should be: `unio_backend.settings`

### To Fix Permanently (Optional)

If you want to set this permanently in your system:

1. Open PowerShell as Administrator
2. Run:
```powershell
[System.Environment]::SetEnvironmentVariable('DJANGO_SETTINGS_MODULE', 'unio_backend.settings', 'User')
```

3. Close and reopen PowerShell

Or simply run the command with the environment variable each time as shown above.

## ✅ What's Working

- ✅ Django server starts successfully
- ✅ Swagger UI generates API documentation
- ✅ All endpoints are documented
- ✅ Database migrations completed
- ✅ SQLite database created

## ⚠️ Known Warnings (Safe to Ignore)

You may see warnings like:
- `UserWarning: pkg_resources is deprecated` - This is from simplejwt and can be ignored
- `MeetingViewSet is not compatible with schema generation` - Already fixed! Schema works fine now

## 🎯 Next Steps

1. **Create a superuser** (if you haven't):
```powershell
python manage.py createsuperuser
```

2. **Open Swagger UI**:
   - Go to http://localhost:8000/swagger/
   - Test the `/api/auth/signup` endpoint to create a user
   - Login at `/api/auth/login` to get your JWT token
   - Click "Authorize" button and enter: `Bearer <your_token>`
   - Test protected endpoints!

3. **Explore the API**:
   - Browse all 30+ endpoints
   - Test each endpoint directly from Swagger
   - See request/response examples
   - No Postman needed!

## 🔧 For WebSocket Support (Advanced)

Currently using Django's built-in server (WSGI) which works for all HTTP endpoints including Swagger.

To enable WebSocket support for real-time features:

1. Uncomment `daphne` in `unio_backend/settings.py` INSTALLED_APPS
2. Start with Daphne:
```powershell
daphne -b 0.0.0.0 -p 8000 unio_backend.asgi:application
```

**Note**: Swagger works fine with regular Django server. Only use Daphne when you need WebSocket functionality.

## 📚 Documentation Files

- **SWAGGER_GUIDE.md** - Comprehensive Swagger usage guide
- **SWAGGER_SETUP.md** - What was added for Swagger
- **README.md** - Complete project documentation
- **QUICKSTART.md** - Quick reference guide

## 🎉 You're Ready!

Your UNIO Backend API with Swagger UI is fully operational!

**Start the server and visit**: http://localhost:8000/swagger/

Enjoy testing your API! 🚀

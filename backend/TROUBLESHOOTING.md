# Troubleshooting Guide

## Common Issues & Solutions

### 1. Server Won't Start

#### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution**:
```bash
pip install -r requirements.txt
```

#### Error: "pydantic_core._pydantic_core.ValidationError"

**Solution**: Check your `.env` file has all required variables:
```env
JWT_SECRET=your_secret
GEMINI_API_KEY=your_key
YOUTUBE_API_KEY=your_key
```

---

### 2. Database Issues

#### SQLite: "OperationalError: no such table"

**Solution**: Tables are auto-created. Restart the server:
```bash
python run.py
```

#### MongoDB: "ServerSelectionTimeoutError"

**Solution**: Start MongoDB:
```bash
mongod
```

Or check `MONGO_URL` in `.env`:
```env
MONGO_URL=mongodb://localhost:27017
```

---

### 3. Authentication Issues

#### Error: "Not authenticated"

**Solutions**:
1. Click "Authorize" button in Swagger
2. Enter: `Bearer <your_token>`
3. Make sure token hasn't expired (30 min default)

#### Error: "Invalid token"

**Solutions**:
1. Login again to get fresh token
2. Check `JWT_SECRET` hasn't changed
3. Verify token format: `Bearer eyJhbGc...`

---

### 4. File Upload Issues

#### Error: "Only PDF files allowed"

**Solution**: Upload `.pdf` files only

#### Error: "Permission denied"

**Solution**: Check `app/storage/uploads/` folder exists and is writable:
```bash
mkdir app\storage\uploads
```

---

### 5. AI Service Issues

#### Error: "API key not valid"

**Solution**: Get valid API keys:
- Gemini: https://makersuite.google.com/app/apikey
- YouTube: https://console.cloud.google.com/

Update `.env`:
```env
GEMINI_API_KEY=AIzaSy...
YOUTUBE_API_KEY=AIzaSy...
```

#### Error: "Timeout"

**Solution**: AI requests can take 10-30 seconds. Be patient or increase timeout in `ai_module_generator.py`:
```python
async with httpx.AsyncClient(timeout=60.0) as client:
```

---

### 6. Database Switching Issues

#### Data not appearing after switch

**Explanation**: SQLite and MongoDB are separate databases. Data doesn't transfer automatically.

**Solution**: 
- Use same database for testing
- Or implement data migration script

#### Error after switching to MongoDB

**Solution**: 
1. Ensure MongoDB is running
2. Check connection string
3. Restart server after changing `.env`

---

### 7. Import Errors

#### Error: "ImportError: cannot import name 'settings'"

**Solution**: Run from `backend/` directory:
```bash
cd backend
python run.py
```

#### Error: "ModuleNotFoundError: No module named 'app'"

**Solution**: Make sure you're in the correct directory:
```bash
cd backend
python run.py
```

---

### 8. Port Already in Use

#### Error: "Address already in use"

**Solution**: Kill process on port 8000:

**Windows**:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Or change port** in `run.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

---

### 9. CORS Issues

#### Error: "CORS policy: No 'Access-Control-Allow-Origin'"

**Solution**: Already configured in `main.py`. If still issues, update:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 10. Swagger Not Loading

#### Blank page at /docs

**Solutions**:
1. Clear browser cache
2. Try `/redoc` instead
3. Check server logs for errors
4. Restart server

---

## Debugging Tips

### Enable Debug Logging

In `config/sqlite.py`:
```python
engine = create_async_engine(settings.SQLITE_DB_URL, echo=True)  # Shows SQL queries
```

### Check Server Logs

Look for errors in terminal where you ran `python run.py`

### Test Individual Components

```python
# Test password hashing
from app.utils.auth_utils import hash_password, verify_password
hashed = hash_password("test123")
print(verify_password("test123", hashed))  # Should be True

# Test JWT
from app.utils.token import create_access_token, verify_token
token = create_access_token({"sub": "1"})
print(verify_token(token))  # Should return payload
```

### Check Database

**SQLite**:
```bash
sqlite3 app.db
.tables
SELECT * FROM users;
```

**MongoDB**:
```bash
mongo
use learning_platform
show collections
db.users.find()
```

---

## Performance Issues

### Slow PDF Processing

**Cause**: Large PDF files

**Solution**: 
- Limit file size in upload route
- Process in background (add Celery later)

### Slow AI Responses

**Cause**: Gemini API latency

**Solution**:
- Cache common responses
- Show loading indicator to user
- Implement timeout handling

---

## Getting Help

1. Check error message in terminal
2. Search error in this guide
3. Check `.env` configuration
4. Verify all dependencies installed
5. Try with fresh database
6. Check API keys are valid

---

## Quick Reset

If everything is broken:

```bash
# Delete database
del app.db  # SQLite

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reset .env
copy .env.example .env
# Edit .env with your keys

# Restart server
python run.py
```

---

## Still Stuck?

Check:
- Python version (3.8+)
- All dependencies installed
- `.env` file exists and has values
- Running from `backend/` directory
- No typos in API keys

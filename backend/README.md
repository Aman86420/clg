# Learning Platform Backend - Production-Ready MVP

## Architecture Overview

This is a production-ready FastAPI backend with **dynamic database switching** between SQLite (local dev) and MongoDB (production).

### Key Features
- ✅ Clean Architecture with Repository Pattern
- ✅ Dynamic Database Switching (SQLite ↔ MongoDB)
- ✅ JWT Authentication with bcrypt
- ✅ PDF Upload & Text Extraction
- ✅ AI Module Generation (Gemini)
- ✅ YouTube Video Recommendations
- ✅ MCQ Submission & Scoring
- ✅ Context-Aware Chatbot

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```env
DATABASE_TYPE=sqlite
SQLITE_DB_URL=sqlite+aiosqlite:///./app.db
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=learning_platform

JWT_SECRET=your_super_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 3. Run the Server

```bash
python run.py
```

Server will start at: `http://localhost:8000`

---

## Database Switching

### Using SQLite (Default - Local Development)

In `.env`:
```env
DATABASE_TYPE=sqlite
```

**Migrations**: SQLite tables are auto-created on startup via SQLAlchemy.

### Using MongoDB (Production)

In `.env`:
```env
DATABASE_TYPE=mongodb
MONGO_URL=mongodb://localhost:27017
```

**No migrations needed** - MongoDB is schemaless.

### How It Works

The `database.py` file detects `DATABASE_TYPE` and returns the appropriate session:

```python
async def get_db():
    if settings.DATABASE_TYPE == "sqlite":
        # Returns SQLAlchemy AsyncSession
    else:
        # Returns Motor MongoDB client
```

**Repositories handle the abstraction** - routes never know which DB is used.

---

## API Documentation

### Swagger UI
Visit: `http://localhost:8000/docs`

### ReDoc
Visit: `http://localhost:8000/redoc`

---

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Upload
- `POST /upload/pdf` - Upload PDF and extract text

### Modules
- `POST /modules/` - Create module manually
- `GET /modules/` - Get all user modules
- `GET /modules/{id}` - Get specific module
- `POST /modules/generate-ai` - Generate AI module from PDF text

### Results
- `POST /results/submit-mcq` - Submit MCQ answers
- `GET /results/my-results` - Get user results
- `GET /results/module/{id}` - Get results for specific module
- `GET /results/analytics` - Get user analytics

### Chatbot
- `POST /chatbot/ask` - Ask question about module

---

## Testing via Swagger

1. **Register**: `POST /auth/register`
```json
{
  "email": "test@example.com",
  "password": "password123",
  "full_name": "Test User"
}
```

2. **Login**: `POST /auth/login`
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Copy the `access_token` from response.

3. **Authorize**: Click "Authorize" button in Swagger, enter:
```
Bearer <your_access_token>
```

4. **Upload PDF**: `POST /upload/pdf`
- Upload a PDF file
- Copy the `extracted_text` from response

5. **Generate AI Module**: `POST /modules/generate-ai`
```json
{
  "extracted_text": "<paste extracted text here>"
}
```

6. **Submit MCQ**: `POST /results/submit-mcq`
```json
{
  "module_id": "1",
  "answers": [0, 1, 2, 0, 1],
  "time_taken": 300
}
```

7. **Ask Chatbot**: `POST /chatbot/ask`
```json
{
  "module_id": "1",
  "question": "What is the main topic?"
}
```

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config/
│   │   ├── settings.py         # Environment config
│   │   ├── database.py         # DB abstraction layer
│   │   ├── sqlite.py           # SQLite setup
│   │   └── mongo.py            # MongoDB setup
│   ├── models/
│   │   ├── sql_models.py       # SQLAlchemy models
│   │   └── mongo_models.py     # MongoDB helpers
│   ├── schemas/
│   │   ├── user_schema.py      # Pydantic schemas
│   │   ├── module_schema.py
│   │   └── result_schema.py
│   ├── repositories/
│   │   ├── user_repository.py  # DB abstraction
│   │   ├── module_repository.py
│   │   └── result_repository.py
│   ├── routes/
│   │   ├── auth_routes.py      # API endpoints
│   │   ├── upload_routes.py
│   │   ├── module_routes.py
│   │   ├── result_routes.py
│   │   └── chatbot_routes.py
│   ├── services/
│   │   ├── pdf_parser.py       # Business logic
│   │   ├── ai_module_generator.py
│   │   ├── youtube_service.py
│   │   ├── mcq_generator.py
│   │   └── result_analyzer.py
│   ├── utils/
│   │   ├── auth_utils.py       # Helpers
│   │   └── token.py
│   └── storage/
│       └── uploads/            # PDF storage
├── requirements.txt
├── .env.example
└── run.py
```

---

## Repository Pattern Explained

Routes → Repositories → Database

**Example Flow**:

1. Route receives request
2. Route calls repository method
3. Repository checks `DATABASE_TYPE`
4. Repository executes SQLite OR MongoDB query
5. Repository returns unified response

**Benefits**:
- Routes are database-agnostic
- Easy to switch databases
- Testable and maintainable

---

## Production Deployment Checklist

- [ ] Change `JWT_SECRET` to strong random value
- [ ] Set `DATABASE_TYPE=mongodb`
- [ ] Configure MongoDB connection string
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure CORS properly
- [ ] Add input validation
- [ ] Set up monitoring

---

## Tech Stack

- **Framework**: FastAPI (async)
- **Databases**: SQLite (SQLAlchemy) + MongoDB (Motor)
- **Auth**: JWT + bcrypt
- **AI**: Google Gemini API
- **PDF**: pdfplumber
- **Video**: YouTube Data API

---

## Notes

- SQLite auto-creates tables on startup
- MongoDB collections are created on first insert
- All passwords are hashed with bcrypt
- JWT tokens expire in 30 minutes (configurable)
- PDF files are stored in `app/storage/uploads/`

---

## Support

For issues or questions, check:
- Swagger docs: `http://localhost:8000/docs`
- Logs in terminal
- `.env` configuration

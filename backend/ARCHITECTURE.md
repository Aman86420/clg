# Architecture Documentation

## System Design

```
┌─────────────┐
│   Client    │
│  (Swagger)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Routes              │
│  (auth, upload, module, result)     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│      Repository Layer               │
│  (Database Abstraction)             │
└──────┬──────────────────────────────┘
       │
       ├──────────┬──────────┐
       ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │ SQLite │ │ MongoDB│ │Services│
   └────────┘ └────────┘ └────────┘
```

---

## Layer Breakdown

### 1. Routes Layer (API Endpoints)

**Responsibility**: Handle HTTP requests/responses

**Files**:
- `auth_routes.py` - Registration, login
- `upload_routes.py` - PDF upload
- `module_routes.py` - Module CRUD
- `result_routes.py` - MCQ submission, analytics
- `chatbot_routes.py` - AI chatbot

**Key Points**:
- Routes are database-agnostic
- Use dependency injection for DB session
- Handle authentication via JWT
- Return Pydantic schemas

---

### 2. Repository Layer (Database Abstraction)

**Responsibility**: Abstract database operations

**Files**:
- `user_repository.py`
- `module_repository.py`
- `result_repository.py`

**Pattern**:
```python
class UserRepository:
    def __init__(self, db):
        self.db = db
        self.db_type = settings.DATABASE_TYPE
    
    async def create_user(self, email, password):
        if self.db_type == "sqlite":
            # SQLAlchemy logic
        else:
            # MongoDB logic
```

**Benefits**:
- Single source of truth for DB operations
- Easy to test (mock repositories)
- Database switching without route changes
- Consistent return format

---

### 3. Database Layer

#### SQLite (SQLAlchemy)

**File**: `config/sqlite.py`

```python
engine = create_async_engine(settings.SQLITE_DB_URL)
async_session_maker = async_sessionmaker(engine)
```

**Models**: `models/sql_models.py`
- User, Module, Result tables
- Foreign key relationships
- Auto-created on startup

#### MongoDB (Motor)

**File**: `config/mongo.py`

```python
mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)
```

**Helpers**: `models/mongo_models.py`
- Document serialization
- ObjectId to string conversion

---

### 4. Service Layer (Business Logic)

**Files**:
- `pdf_parser.py` - Extract text from PDF
- `ai_module_generator.py` - Call Gemini API
- `youtube_service.py` - Search YouTube
- `mcq_generator.py` - Calculate scores
- `result_analyzer.py` - Generate analytics

**Characteristics**:
- Pure business logic
- No database knowledge
- Reusable across routes
- Easy to unit test

---

### 5. Schema Layer (Validation)

**Files**:
- `user_schema.py`
- `module_schema.py`
- `result_schema.py`

**Purpose**:
- Request validation
- Response serialization
- Type safety
- Auto-generated API docs

---

## Database Switching Mechanism

### Configuration (`config/database.py`)

```python
async def get_db():
    if settings.DATABASE_TYPE == "sqlite":
        async for session in get_sqlite_session():
            yield session
    else:
        yield await get_mongo_db()
```

### Repository Implementation

```python
async def create_user(self, email, hashed_password):
    if self.db_type == "sqlite":
        user = SQLUser(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        return {"id": str(user.id), "email": user.email}
    else:
        user_doc = {"email": email, "hashed_password": hashed_password}
        result = await self.db.users.insert_one(user_doc)
        return {"id": str(result.inserted_id), "email": email}
```

**Key**: Both branches return the same structure!

---

## Authentication Flow

```
1. User registers → Password hashed with bcrypt
2. User logs in → Password verified
3. JWT token generated with user_id
4. Token sent in Authorization header
5. Token verified on protected routes
6. User ID extracted from token
7. Used for database queries
```

**Implementation**:
- `auth_utils.py` - Password hashing
- `token.py` - JWT creation/verification
- `get_current_user()` - Dependency for protected routes

---

## AI Integration

### PDF → Module Flow

```
1. Upload PDF → Saved to storage/uploads/
2. Extract text → pdfplumber
3. Send to Gemini → AI generates module
4. Search YouTube → Get video recommendation
5. Save to database → Module with MCQs
```

### Chatbot Flow

```
1. User asks question
2. Fetch module from database
3. Build context (title + content + PDF text)
4. Send to Gemini with question
5. Return AI response
```

---

## Data Models

### SQLite Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    created_at DATETIME
);

CREATE TABLE modules (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    pdf_text TEXT,
    video_id VARCHAR,
    created_at DATETIME
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    module_id INTEGER REFERENCES modules(id),
    score FLOAT NOT NULL,
    total_questions INTEGER NOT NULL,
    time_taken INTEGER,
    created_at DATETIME
);
```

### MongoDB Collections

```javascript
// users
{
  _id: ObjectId,
  email: String,
  hashed_password: String,
  full_name: String,
  created_at: Date
}

// modules
{
  _id: ObjectId,
  user_id: ObjectId,
  title: String,
  content: String,
  pdf_text: String,
  video_id: String,
  created_at: Date
}

// results
{
  _id: ObjectId,
  user_id: ObjectId,
  module_id: ObjectId,
  score: Float,
  total_questions: Integer,
  time_taken: Integer,
  created_at: Date
}
```

---

## Design Patterns Used

1. **Repository Pattern** - Database abstraction
2. **Dependency Injection** - DB session, current user
3. **Strategy Pattern** - Database switching
4. **Service Layer** - Business logic separation
5. **DTO Pattern** - Pydantic schemas

---

## Scalability Considerations

### Current MVP
- Single server
- Local file storage
- Synchronous AI calls

### Production Enhancements
- Add Redis for caching
- Use S3 for file storage
- Add Celery for async tasks
- Implement rate limiting
- Add database indexing
- Use connection pooling
- Add load balancer

---

## Security Features

✅ Password hashing (bcrypt)
✅ JWT authentication
✅ Token expiration
✅ Input validation (Pydantic)
✅ SQL injection prevention (SQLAlchemy)
✅ CORS configuration

**TODO for Production**:
- Rate limiting
- HTTPS only
- API key rotation
- Input sanitization
- File upload limits
- Request logging

---

## Testing Strategy

### Unit Tests
- Test repositories with mock DB
- Test services independently
- Test utilities (auth, token)

### Integration Tests
- Test routes with test database
- Test database switching
- Test AI service integration

### E2E Tests
- Full user flow
- Database migration
- API contract testing

---

## Why This Architecture?

### Clean Separation
- Easy to understand
- Easy to maintain
- Easy to test

### Database Flexibility
- Switch without code changes
- Support multiple databases
- Easy to add new databases

### Production Ready
- Async operations
- Proper error handling
- Scalable structure
- Industry standards

---

## Comparison: College Project vs This

| Feature | College Project | This MVP |
|---------|----------------|----------|
| Architecture | Monolithic | Layered |
| Database | Hardcoded | Pluggable |
| Auth | Basic | JWT + bcrypt |
| Code Quality | Mixed | Clean |
| Testability | Hard | Easy |
| Scalability | Limited | High |
| Maintainability | Low | High |

This is **internship/junior dev level** architecture! 🚀

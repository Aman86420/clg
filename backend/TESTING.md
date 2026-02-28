# API Testing Guide

## Complete Flow Test

### Step 1: Register User

**Endpoint**: `POST /auth/register`

```json
{
  "email": "student@example.com",
  "password": "secure123",
  "full_name": "John Doe"
}
```

**Response**:
```json
{
  "id": "1",
  "email": "student@example.com",
  "full_name": "John Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Step 2: Login

**Endpoint**: `POST /auth/login`

```json
{
  "email": "student@example.com",
  "password": "secure123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Important**: Copy the `access_token` and use it in all subsequent requests.

---

### Step 3: Authorize in Swagger

1. Click the **"Authorize"** button (top right)
2. Enter: `Bearer <your_access_token>`
3. Click "Authorize"

---

### Step 4: Upload PDF

**Endpoint**: `POST /upload/pdf`

- Select a PDF file
- Click "Execute"

**Response**:
```json
{
  "filename": "lecture.pdf",
  "file_path": "app/storage/uploads/1_lecture.pdf",
  "extracted_text": "This is the beginning of the PDF text...",
  "full_text_length": 5000
}
```

**Copy the full extracted text** (you'll need it for next step).

---

### Step 5: Generate AI Module

**Endpoint**: `POST /modules/generate-ai`

```json
{
  "extracted_text": "<paste the full extracted text here>"
}
```

**Response**:
```json
{
  "module": {
    "id": "1",
    "user_id": "1",
    "title": "Introduction to Machine Learning",
    "content": "Machine learning is...",
    "pdf_text": "...",
    "video_id": "dQw4w9WgXcQ",
    "created_at": "2024-01-01T00:00:00"
  },
  "mcqs": [
    {
      "question": "What is supervised learning?",
      "options": ["A", "B", "C", "D"],
      "correct": 0
    }
  ],
  "video_id": "dQw4w9WgXcQ"
}
```

**Note the module ID** (e.g., "1").

---

### Step 6: Get All Modules

**Endpoint**: `GET /modules/`

**Response**:
```json
[
  {
    "id": "1",
    "user_id": "1",
    "title": "Introduction to Machine Learning",
    "content": "...",
    "pdf_text": "...",
    "video_id": "dQw4w9WgXcQ",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### Step 7: Submit MCQ Answers

**Endpoint**: `POST /results/submit-mcq`

```json
{
  "module_id": "1",
  "answers": [0, 1, 2, 0, 1],
  "time_taken": 300
}
```

**Response**:
```json
{
  "id": "1",
  "user_id": "1",
  "module_id": "1",
  "score": 80.0,
  "total_questions": 5,
  "time_taken": 300,
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Step 8: Get Results

**Endpoint**: `GET /results/my-results`

**Response**:
```json
[
  {
    "id": "1",
    "user_id": "1",
    "module_id": "1",
    "score": 80.0,
    "total_questions": 5,
    "time_taken": 300,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### Step 9: Get Analytics

**Endpoint**: `GET /results/analytics`

**Response**:
```json
{
  "average_score": 80.0,
  "total_attempts": 1,
  "best_score": 80.0,
  "latest_score": 80.0
}
```

---

### Step 10: Ask Chatbot

**Endpoint**: `POST /chatbot/ask`

```json
{
  "module_id": "1",
  "question": "What are the main types of machine learning?"
}
```

**Response**:
```json
{
  "question": "What are the main types of machine learning?",
  "answer": "Based on the module content, the main types of machine learning are: 1. Supervised Learning, 2. Unsupervised Learning, 3. Reinforcement Learning..."
}
```

---

## Database Switching Test

### Test with SQLite

1. In `.env`, set:
```env
DATABASE_TYPE=sqlite
```

2. Restart server
3. Run all tests above
4. Check `app.db` file is created

### Test with MongoDB

1. Start MongoDB:
```bash
mongod
```

2. In `.env`, set:
```env
DATABASE_TYPE=mongodb
```

3. Restart server
4. Run all tests above
5. Check MongoDB collections:
```bash
mongo
use learning_platform
show collections
db.users.find()
```

---

## Expected Behavior

✅ Routes work identically with both databases
✅ No code changes needed to switch
✅ Repository layer handles all differences
✅ Data structure remains consistent

---

## Troubleshooting

### "Not authenticated" error
- Make sure you clicked "Authorize" in Swagger
- Check token format: `Bearer <token>`

### "Module not found" error
- Verify module_id from previous response
- Check you're using the correct user

### Database connection error
- SQLite: Check file permissions
- MongoDB: Ensure MongoDB is running

### API key errors
- Verify GEMINI_API_KEY in .env
- Verify YOUTUBE_API_KEY in .env

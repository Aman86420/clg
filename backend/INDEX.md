# 📚 Documentation Index

Welcome to the Learning Platform Backend documentation!

## 🚀 Getting Started

Start here if you're new:

1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
2. **[README.md](README.md)** - Complete overview and setup guide
3. **[TESTING.md](TESTING.md)** - Test all API endpoints

## 📖 Core Documentation

### For Developers

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and patterns explained
  - Repository Pattern
  - Database Abstraction
  - Layer Breakdown
  - Design Patterns Used

- **[FLOW_DIAGRAMS.md](FLOW_DIAGRAMS.md)** - Visual flow diagrams
  - Authentication Flow
  - PDF Upload Flow
  - MCQ Submission Flow
  - Chatbot Flow
  - Database Switching

### For Operations

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
  - Server Setup
  - Docker Deployment
  - Cloud Options (AWS, GCP, Heroku)
  - Security Hardening
  - Monitoring Setup

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
  - Server Issues
  - Database Problems
  - Authentication Errors
  - API Service Issues

## 📋 Quick Reference

### Project Structure
```
backend/
├── app/
│   ├── config/          # Database & settings
│   ├── models/          # SQLAlchemy & MongoDB models
│   ├── schemas/         # Pydantic validation
│   ├── repositories/    # Database abstraction
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── utils/           # Helpers
├── requirements.txt     # Dependencies
├── .env                 # Configuration
└── run.py              # Server starter
```

### Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application entry point |
| `app/config/database.py` | Database switching logic |
| `app/config/settings.py` | Environment configuration |
| `run.py` | Server startup script |
| `.env` | Environment variables |

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | Login and get JWT |
| `/upload/pdf` | POST | Upload PDF file |
| `/modules/generate-ai` | POST | Generate AI module |
| `/modules/` | GET | Get user modules |
| `/results/submit-mcq` | POST | Submit quiz answers |
| `/results/my-results` | GET | Get user results |
| `/chatbot/ask` | POST | Ask AI chatbot |

## 🎯 By Use Case

### "I want to understand the architecture"
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

### "I want to deploy to production"
→ Follow [DEPLOYMENT.md](DEPLOYMENT.md)

### "I'm getting an error"
→ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### "I want to test the API"
→ Follow [TESTING.md](TESTING.md)

### "I want to see how data flows"
→ View [FLOW_DIAGRAMS.md](FLOW_DIAGRAMS.md)

### "I just want to run it"
→ Follow [QUICKSTART.md](QUICKSTART.md)

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_TYPE=sqlite          # or mongodb
SQLITE_DB_URL=sqlite+aiosqlite:///./app.db
MONGO_URL=mongodb://localhost:27017

# Security
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
GEMINI_API_KEY=your_gemini_key
YOUTUBE_API_KEY=your_youtube_key
```

### Database Switching

**SQLite** (Local Development):
```env
DATABASE_TYPE=sqlite
```

**MongoDB** (Production):
```env
DATABASE_TYPE=mongodb
MONGO_URL=mongodb://localhost:27017
```

## 🏗️ Architecture Highlights

### Repository Pattern
Routes → Repositories → Database

**Benefits**:
- Database-agnostic routes
- Easy to test
- Switch databases without code changes

### Clean Architecture
- **Routes**: HTTP handling
- **Repositories**: Database abstraction
- **Services**: Business logic
- **Models**: Data structures
- **Schemas**: Validation

### Security
- JWT authentication
- bcrypt password hashing
- Token expiration
- Input validation

## 📊 Features Implemented

✅ User registration & login  
✅ JWT authentication  
✅ PDF upload & text extraction  
✅ AI module generation (Gemini)  
✅ YouTube video recommendations  
✅ MCQ submission & scoring  
✅ Result analytics  
✅ Context-aware chatbot  
✅ Dynamic database switching  

## 🎓 Learning Resources

### Concepts Covered
- FastAPI async patterns
- Repository Pattern
- Database abstraction
- JWT authentication
- Clean Architecture
- Dependency Injection

### Technologies Used
- **Framework**: FastAPI
- **Databases**: SQLite (SQLAlchemy) + MongoDB (Motor)
- **Auth**: JWT + bcrypt
- **AI**: Google Gemini
- **PDF**: pdfplumber
- **Video**: YouTube Data API

## 🆘 Getting Help

1. **Check documentation** - Start with relevant doc above
2. **Check logs** - Look at terminal output
3. **Verify config** - Check `.env` file
4. **Test endpoints** - Use Swagger at `/docs`
5. **Check troubleshooting** - See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📞 Quick Commands

### Start Server
```bash
python run.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### View API Docs
```
http://localhost:8000/docs
```

### Check Health
```
http://localhost:8000/health
```

## 🎯 Next Steps

### For Learning
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study [FLOW_DIAGRAMS.md](FLOW_DIAGRAMS.md)
3. Test API via [TESTING.md](TESTING.md)

### For Development
1. Follow [QUICKSTART.md](QUICKSTART.md)
2. Test all endpoints
3. Modify and extend

### For Production
1. Review [DEPLOYMENT.md](DEPLOYMENT.md)
2. Configure environment
3. Set up monitoring
4. Deploy!

## 📝 Summary

This is a **production-ready MVP** with:
- ✅ Clean architecture
- ✅ Database flexibility
- ✅ Security best practices
- ✅ Comprehensive documentation
- ✅ Industry-standard patterns

**You're ready to build, deploy, and scale!** 🚀

---

## 📄 All Documentation Files

1. [README.md](README.md) - Main documentation
2. [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
3. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. [TESTING.md](TESTING.md) - API testing guide
5. [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
6. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
7. [FLOW_DIAGRAMS.md](FLOW_DIAGRAMS.md) - Visual diagrams
8. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
9. [INDEX.md](INDEX.md) - This file

---

Made with ❤️ for learning and growth

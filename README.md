# Learning Platform - AI-Powered Educational System

An intelligent learning platform that converts PDF documents into interactive learning modules with AI-generated content, YouTube video recommendations, and automated MCQ generation.

## 🚀 Features

- **PDF Upload & Text Extraction**: Upload PDF documents and extract text content
- **AI-Powered Module Generation**: Automatically generate structured learning modules using Google Gemini AI
- **YouTube Integration**: Automatically find and recommend relevant educational videos
- **MCQ Generation**: AI-generated multiple-choice questions for knowledge assessment
- **User Authentication**: Secure JWT-based authentication system
- **RESTful API**: Clean and well-documented API endpoints

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: Google Gemini API
- **Video Search**: YouTube Data API
- **PDF Processing**: PDFPlumber
- **Authentication**: JWT (JSON Web Tokens)

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key
- YouTube Data API Key

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Aman86420/clg.git
cd clg
```

2. **Navigate to backend directory**
```bash
cd backend
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the `backend` directory:
```env
DATABASE_TYPE=sqlite
SQLITE_DB_URL=sqlite+aiosqlite:///./app.db
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=learning_platform

JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

5. **Run the application**
```bash
python run.py
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Test API Connectivity
```bash
python test_apis.py
```

### Complete Testing Guide
See [TESTING_GUIDE.md](backend/TESTING_GUIDE.md) for detailed testing instructions.

## 📖 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Upload
- `POST /upload/pdf` - Upload PDF and extract text

### Modules
- `POST /modules/generate-ai` - Generate AI module with MCQs and YouTube video
- `GET /modules/` - Get user's modules
- `GET /modules/{module_id}` - Get specific module

### Health Check
- `GET /` - API status
- `GET /health` - Health check

## 🔄 Workflow

1. **Register/Login** → Get JWT token
2. **Upload PDF** → Extract text content
3. **Generate Module** → AI creates:
   - Structured learning content
   - Relevant YouTube video link
   - Multiple-choice questions
4. **Access Module** → Retrieve and study the generated content

## 📁 Project Structure

```
clg-project/
└── backend/
    ├── app/
    │   ├── config/         # Configuration files
    │   ├── models/         # Database models
    │   ├── repositories/   # Data access layer
    │   ├── routes/         # API endpoints
    │   ├── schemas/        # Pydantic schemas
    │   ├── services/       # Business logic
    │   ├── storage/        # File storage
    │   ├── utils/          # Utility functions
    │   └── main.py         # Application entry point
    ├── .env                # Environment variables (not in git)
    ├── requirements.txt    # Python dependencies
    └── run.py             # Server startup script
```

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- API key protection via environment variables
- Input validation with Pydantic

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Aman**
- GitHub: [@Aman86420](https://github.com/Aman86420)

## 🙏 Acknowledgments

- Google Gemini AI for content generation
- YouTube Data API for video recommendations
- FastAPI framework for the robust backend

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ by Aman

# Quick Start Guide

## 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## 2. Setup Environment

```bash
copy .env.example .env
```

Edit `.env` and add your API keys (minimum required):
- `JWT_SECRET` - Any random string
- `GEMINI_API_KEY` - Get from Google AI Studio
- `YOUTUBE_API_KEY` - Get from Google Cloud Console

## 3. Run Server

```bash
python run.py
```

## 4. Test API

Open browser: `http://localhost:8000/docs`

## Switch Database

### SQLite (Default)
```env
DATABASE_TYPE=sqlite
```

### MongoDB
```env
DATABASE_TYPE=mongodb
MONGO_URL=mongodb://localhost:27017
```

That's it! 🚀

# Backend Implementation Plan (Developer 2)

## Goal
Build the MERN backend for LMS MVP: auth, session lifecycle, PDF ingestion, AI analysis → module breakdown, quizzes, analytics, and AI chat support.

## Tech Stack (Fast & Scalable)
- **Node.js + Express** (API)
- **MongoDB + Mongoose** (data store)
- **Redis** (queues, caching, session state)
- **BullMQ / RabbitMQ** (async jobs for AI analysis)
- **OpenAI / Azure OpenAI / local LLM** (content analysis + module split)
- **PDF ingestion**: pdf-parse + OCR fallback (Tesseract) if needed
- **File Storage**: S3-compatible (MinIO for dev)
- **Auth**: JWT + refresh tokens
- **Real-time**: SSE or WebSockets for AI chat streaming

## Core Features (MVP)
1. **Auth + Session Start**
   - Login/Signup
   - Start a learning session (create session ID)
2. **Upload APIs**
   - Two PDFs: Notes + PYQ
   - Validate & store with metadata
3. **AI Analysis Pipeline**
   - Extract text from PDFs
   - Summarize subject & split into modules
   - Generate key notes + suggested videos
   - Store modules linked to session
4. **Module APIs**
   - List modules
   - Get module details (video, notes, goals)
5. **Quiz System**
   - Generate module quiz from notes
   - Save quiz attempts and scoring
6. **Performance Analytics**
   - Aggregated stats by module/session
   - Time taken, accuracy, trend data
7. **AI Doubt Solver**
   - Chat endpoint with context: current video + notes
   - Streamed response (SSE/WS)

## Data Models (Mongo)
- **User**: profile, auth, preferences
- **Session**: userId, subject, status, createdAt
- **Document**: sessionId, type (notes/pyq), storageRef
- **Module**: sessionId, title, goals, videoUrl, notesSummary
- **Quiz**: moduleId, questions, correctAnswers
- **QuizAttempt**: quizId, userId, score, timeTaken
- **Analytics**: userId, sessionId, metrics

## API Endpoints (Proposed)
- `POST /auth/login`
- `POST /auth/register`
- `POST /session/start`
- `POST /session/:id/upload` (notes/pyq)
- `GET /session/:id/modules`
- `GET /modules/:id`
- `POST /modules/:id/quiz`
- `POST /quiz/:id/submit`
- `GET /analytics/:sessionId`
- `POST /chat` (SSE/WS)

## Async Processing Pipeline
1. Upload PDFs
2. Extract text (pdf-parse / OCR)
3. LLM module splitting
4. Save modules + summaries
5. Create quiz question set per module

## Performance Dashboard Support
- Store quiz attempt metrics
- Precompute aggregates in `Analytics` collection
- API supports time series and per-module drilldowns

## Milestones
1. **Week 1**: Auth + session + upload + storage
2. **Week 2**: AI analysis pipeline + module generation
3. **Week 3**: Quiz system + analytics + chat streaming

## Definition of Done
- End-to-end flow from upload → module list
- Quiz generation + scoring works
- Performance endpoint returns chart-ready data
- AI chat returns streaming answer with context

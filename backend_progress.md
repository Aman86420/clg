# Backend Progress Tracker

## How to Use
- Mark each task as **Not Started**, **In Progress**, or **Done**.
- Add dates and brief notes in the **Daily Notes** section.
- Keep tasks small and achievable for daily momentum.

---

## Day 1 — Detailed Plan (Tech Stack + Setup)

### Tech Stack (Decision + Rationale)
- **Node.js (LTS) + Express**: fast to build REST APIs and fits MERN.
- **MongoDB + Mongoose**: flexible schema for evolving modules/analytics.
- **Redis**: caching + job queue coordination.
- **BullMQ**: background jobs for PDF ingestion and AI analysis.
- **S3-compatible storage (MinIO in dev)**: store uploaded PDFs.
- **LLM Provider (OpenAI or Azure OpenAI)**: module splitting + notes/quiz generation.
- **pdf-parse**: extract text from PDFs; add OCR later if needed.
- **JWT auth**: access + refresh tokens.
- **SSE**: stream AI chat responses.

### Day 1 Tasks (Detailed)
1. **Initialize Backend Repo Structure**
   - Create `server/` folder structure: `src`, `routes`, `controllers`, `models`, `services`, `jobs`, `utils`.
   - Add `package.json` with scripts: `dev`, `start`, `lint`.
2. **Set Up Core Dependencies**
   - Install: `express`, `cors`, `dotenv`, `mongoose`, `jsonwebtoken`, `bcrypt`, `multer`, `pdf-parse`.
   - Install dev: `nodemon`, `eslint`, `prettier`.
3. **Add Environment Configuration**
   - Create `.env.example` with DB, JWT, Redis, and S3 keys.
4. **Create Base Server**
   - `app.js` with JSON parsing, CORS, error handler.
   - Health check route: `GET /health`.
5. **Database Connection**
   - Add `db.js` for Mongo connection.
6. **Define Initial Models**
   - `User`, `Session`, `Document` schemas (basic fields).
7. **Daily Notes**
   - Add progress notes and blockers.

---

## Day 2
- Auth endpoints (register/login) + JWT issuance.
- Password hashing + validation.

## Day 3
- Session start endpoint + basic session model.

## Day 4
- Upload endpoints (notes + pyq) with file storage stub.

## Day 5
- PDF text extraction service + job queue stub.

## Day 6
- AI analysis job: module split + summary generation (mocked).

## Day 7
- Module APIs: list + detail endpoints.

## Day 8
- Quiz generation service (mocked questions).

## Day 9
- Quiz submission endpoint + scoring.

## Day 10
- Analytics aggregation endpoint.

## Day 11
- AI chat streaming endpoint (SSE).

## Day 12
- Hardening: validation, logging, and error handling.

## Day 13
- Performance tuning + caching with Redis.

## Day 14
- End-to-end dry run + docs update.

---

## Daily Notes
- Day 1: 
- Day 2: 
- Day 3: 
- Day 4: 
- Day 5: 
- Day 6: 
- Day 7: 
- Day 8: 
- Day 9: 
- Day 10: 
- Day 11: 
- Day 12: 
- Day 13: 
- Day 14: 

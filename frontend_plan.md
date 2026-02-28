# Frontend Implementation Plan (Developer 1)

## Goal
Build the learner-facing LMS MVP experience: session onboarding, module dashboard UI, media/notes display, quiz entry, AI chat panel, and performance dashboards.

## Tech Stack (MERN + fast UI)
- **React + Vite** (fast dev/build)
- **TypeScript** (safer UI contracts)
- **Tailwind CSS + Headless UI** (rapid layout & accessible components)
- **React Router** (routing)
- **TanStack Query** (data fetching + caching)
- **Zustand** (lightweight state for session/module UI state)
- **Charting**: Recharts or ECharts
- **Video**: HTML5 video player + HLS.js (if streaming)

## Feature Scope (MVP)
1. **Auth Flow**
   - Login page (mock or API-backed)
   - Start session screen after login
2. **Upload UI**
   - Two required PDF uploads: Notes + PYQ
   - Progress indicator + validation
3. **Module Dashboard (3-column layout)**
   - **Column 1 (Nav):** Dashboard, Analysis, Quiz Scores, Break, Performance, placeholders for future
   - **Column 2 (Learning):**
     - Video box (AI-suggested video, no redirect)
     - Important notes (AI summarized)
     - Button: Start Quiz (current module)
   - **Column 3 (AI Bot):**
     - Chat interface with context (video + notes)
4. **Performance Dashboard**
   - Charts: progress over time, quiz scores, time taken, accuracy, topic coverage
   - Placeholder panels for future metrics

## UI/UX Deliverables
- Design system tokens (colors, spacing, typography)
- Responsive layout (desktop-first, tablet-friendly)
- Skeleton loaders for async data
- Empty states: no modules, no video, no notes
- Error states: upload failure, module load failure

## Pages & Components
### Pages
- `/login`
- `/session/start`
- `/session/upload`
- `/dashboard` (default module view)
- `/performance`
- `/analysis`
- `/quiz-scores`

### Core Components
- `AppShell`: layout with 3-column grid
- `LeftNav`: nav + placeholder for future
- `VideoPlayer`: embedded video area
- `NotesPanel`: highlights + summaries
- `QuizCTA`: start quiz button
- `AIBotPanel`: chat UI (streaming-ready)
- `ModuleList`: module cards
- `PerformanceCharts`: multi-chart grid

## Data Contracts (from Backend)
- Auth: token + user profile
- Upload: signed URL or direct upload endpoint
- Module list: id, title, learning goals, video URL, notes
- Quiz stats: score, time, attempts, topic breakdown
- Chat: SSE/WebSocket for streaming answers

## Integration Plan
1. **Mock API** with MSW to unblock UI
2. **Replace mock with real APIs** as backend lands
3. **Streamed responses** in AI chat (SSE)
4. **Video + notes sync** by module selection

## Milestones
1. **Week 1**: Auth + session flow + upload UI
2. **Week 2**: Dashboard layout + AI bot UI + module switch
3. **Week 3**: Performance dashboards + polish + error states

## Definition of Done
- All screens functional with mocked data
- API contracts documented in frontend README
- Responsive layout with accessibility baseline (focus states, ARIA)
- Performance dashboard showing charts from mock/real data

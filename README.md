# Todox

A modern task management application with priorities, deadlines, and custom labels.

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Next.js | 15+ |
| | TypeScript | 5.x |
| | Shadcn UI | Latest |
| | Tailwind CSS | 4.x |
| | React Query | 5.x |
| **Backend** | FastAPI | 0.104+ |
| | Python | 3.11+ |
| | Motor (MongoDB) | 3.3+ |
| | Pydantic | 2.5+ |
| **Database** | MongoDB Atlas | 7.0+ |
| **Deployment** | Vercel (Frontend) | - |
| | Railway (Backend) | - |

## Prerequisites

- Node.js 18+ and npm 10+
- Python 3.11+
- MongoDB Atlas account (free tier available)

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT secret
   ```

5. **Run development server:**
   ```bash
   uvicorn src.main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env.local
   # Default API URL is already configured
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## Development Commands

### Backend

```bash
# Run development server
uvicorn src.main:app --reload

# Run tests
pytest

# Lint code
ruff check src/

# Type check
mypy src/
```

### Frontend

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set root directory to `frontend`
3. Configure environment variable: `NEXT_PUBLIC_API_URL` (your Railway backend URL)
4. Deploy

### Backend (Railway)

1. Connect your GitHub repository to Railway
2. Configure environment variables (see `backend/.env.example`)
3. Railway will auto-detect FastAPI and deploy

## Documentation

- **API Documentation:** `http://localhost:8000/docs` (when backend is running)
- **Project Documentation:** See `/docs` directory
  - Product Requirements: `docs/prd.md`
  - Architecture: `docs/architecture.md`
  - Frontend Spec: `docs/front-end-spec.md`
  - User Stories: `docs/stories/`

## Project Structure

```
todox/
├── frontend/          # Next.js application
│   └── src/
│       ├── app/       # App Router pages
│       ├── components/
│       ├── lib/
│       ├── hooks/
│       └── types/
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── api/       # API routes
│   │   ├── services/  # Business logic
│   │   ├── models/    # Data models
│   │   └── core/      # Core utilities
│   └── tests/
├── e2e/              # Playwright E2E tests
└── docs/             # Project documentation
```

## License

MIT
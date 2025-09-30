# Todox

A modern task management application with priorities, deadlines, and custom labels.

## 🌐 Live Demo

**Frontend:** https://frontend-dikdicjca-dres-projects-71e8c4e5.vercel.app  
**Backend API:** https://todox-backend-production.up.railway.app  
**API Docs:** https://todox-backend-production.up.railway.app/docs

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

### Backend (Railway)

**Step 1: Create Railway Project**
1. Sign up at [Railway](https://railway.app)
2. Create new project and connect your GitHub repository
3. Railway will automatically detect Python/FastAPI

**Step 2: Configure Environment Variables**

In Railway dashboard, add these environment variables:

```
MONGODB_URI=mongodb+srv://your-username:password@cluster.mongodb.net/todox?retryWrites=true&w=majority
JWT_SECRET=your-production-secret-32-chars-minimum
JWT_EXPIRES_IN=3600
JWT_ALGORITHM=HS256
CORS_ORIGINS=https://your-app.vercel.app
```

**Step 3: Deploy**
- Railway deploys automatically on push to main
- Note your Railway URL (e.g., `https://todox-backend.up.railway.app`)
- Test health check: `curl https://your-railway-url.up.railway.app/health`

### Frontend (Vercel)

**Step 1: Create Vercel Project**
1. Sign up at [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Vercel will automatically detect Next.js

**Step 2: Configure Project Settings**
- Set **Root Directory** to `frontend`
- Framework Preset: Next.js (auto-detected)

**Step 3: Configure Environment Variables**

Add in Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app
```

**Step 4: Deploy**
- Vercel deploys automatically on push to main
- Get your production URL (e.g., `https://todox.vercel.app`)

**Step 5: Update CORS**
- Go back to Railway dashboard
- Update `CORS_ORIGINS` to include your Vercel URL:
  ```
  CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
  ```

### E2E Testing

**Run tests locally:**
```bash
cd e2e
npm test
```

**Test against production:**
```bash
E2E_BASE_URL=https://your-app.vercel.app npm test
```

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
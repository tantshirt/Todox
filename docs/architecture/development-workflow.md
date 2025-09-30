# Development Workflow

## Local Development Setup

### Prerequisites

```bash
# System requirements
node --version    # v18+ required
python --version  # 3.11+ required
npm --version     # 10+ required
pip --version     # 23+ required

# Install MongoDB Compass (optional, for local DB viewing)
# Or use MongoDB MCP in your IDE
```

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/todox.git
cd todox

# Frontend setup
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set:
# - MONGODB_URI (your MongoDB Atlas connection string)
# - JWT_SECRET (generate with: openssl rand -hex 32)
# - CORS_ORIGINS=http://localhost:3000

# E2E tests setup (optional for initial dev)
cd ../e2e
npm install
```

### Development Commands

```bash
# Start backend (from backend/ directory)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (from frontend/ directory)
npm run dev
# Opens at http://localhost:3000

# Run backend tests (from backend/)
pytest

# Run E2E tests (from e2e/, requires both servers running)
npx playwright test
npx playwright test --ui  # Interactive mode

# Linting and type checking
# Frontend
npm run lint
npm run type-check

# Backend
mypy src/
ruff check src/
```

## Environment Configuration

### Required Environment Variables

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn-here

# Backend (.env)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/todox?retryWrites=true&w=majority
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=3600
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000

# Optional
SENTRY_DSN=your-sentry-dsn-here
```

---

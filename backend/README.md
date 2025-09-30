# Todox Backend

FastAPI backend for the Todox task management application.

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Development

**Run development server:**
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Testing

**Run tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=src tests/
```

## Linting and Type Checking

**Lint code:**
```bash
ruff check src/
```

**Type check:**
```bash
mypy src/
```

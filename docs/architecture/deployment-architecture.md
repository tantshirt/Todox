# Deployment Architecture

## Deployment Strategy

**Frontend Deployment:**
- **Platform:** Vercel
- **Build Command:** `cd frontend && npm run build`
- **Output Directory:** `frontend/.next`
- **CDN/Edge:** Vercel Edge Network (automatic)
- **Automatic Deployments:** Push to `main` branch triggers production deploy, PRs create preview URLs

**Backend Deployment:**
- **Platform:** Railway
- **Build Command:** `pip install -r requirements.txt` (automatic)
- **Deployment Method:** Docker container or Nixpacks (Railway automatic detection)
- **Automatic Deployments:** Git tag push triggers production deploy (e.g., `git tag v1.0.0 && git push origin v1.0.0`)

## CI/CD Pipeline

```yaml
# .github/workflows/ci.yml - Continuous Integration

name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  frontend-lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Lint
        working-directory: ./frontend
        run: npm run lint
      - name: Type check
        working-directory: ./frontend
        run: npm run type-check
  
  backend-lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Lint with ruff
        working-directory: ./backend
        run: ruff check src/
      - name: Type check with mypy
        working-directory: ./backend
        run: mypy src/
      - name: Run tests
        working-directory: ./backend
        run: pytest
        env:
          MONGODB_URI: ${{ secrets.MONGODB_URI_TEST }}
          JWT_SECRET: test-secret-key

  e2e-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - name: Install Playwright
        working-directory: ./e2e
        run: |
          npm ci
          npx playwright install --with-deps
      - name: Run E2E tests
        working-directory: ./e2e
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: e2e/playwright-report/
```

## Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|--------------|-------------|---------|
| Development | http://localhost:3000 | http://localhost:8000 | Local development |
| Staging | N/A (preview URLs) | N/A (Railway preview) | PR previews (optional) |
| Production | https://todox.vercel.app | https://todox-backend.up.railway.app | Live environment |

---

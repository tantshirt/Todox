# Unified Project Structure

```plaintext
todox/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint and test on PR
│       └── deploy.yml                # Deploy on tag (backend) and push (frontend)
│
├── frontend/                         # Next.js application
│   ├── src/
│   │   ├── app/                      # App Router pages
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   ├── tasks/page.tsx
│   │   │   └── labels/page.tsx
│   │   ├── components/               # React components
│   │   │   ├── ui/                   # Shadcn primitives
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   └── labels/
│   │   ├── lib/                      # Utilities
│   │   │   ├── api.ts
│   │   │   ├── auth.tsx
│   │   │   └── utils.ts
│   │   ├── hooks/                    # Custom hooks
│   │   ├── types/                    # TypeScript types
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   ├── .env.local                    # Local env vars (gitignored)
│   ├── .env.example
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── components.json               # Shadcn config
│   └── package.json
│
├── backend/                          # FastAPI application
│   ├── src/
│   │   ├── main.py                   # App entry point
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── tasks.py
│   │   │       └── labels.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   └── label_service.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── task_repository.py
│   │   │   └── label_repository.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── label.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── task.py
│   │   │   └── label.py
│   │   └── middleware/
│   │       ├── auth_middleware.py
│   │       └── cors_middleware.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_labels.py
│   ├── .env                          # Local env vars (gitignored)
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── e2e/                              # Playwright E2E tests
│   ├── tests/
│   │   ├── auth.spec.ts
│   │   ├── tasks.spec.ts
│   │   └── labels.spec.ts
│   ├── playwright.config.ts
│   └── package.json
│
├── docs/                             # Project documentation
│   ├── prd.md
│   ├── front-end-spec.md
│   ├── architecture.md               # This file
│   └── README.md
│
├── .gitignore
├── README.md                         # Root README with setup instructions
└── LICENSE
```

---

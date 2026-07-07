# OptiCrop

OptiCrop is a smart agricultural production optimization engine that recommends crops based on soil and environmental conditions. It includes a FastAPI backend, a React frontend, SQLite persistence, and a simple authentication flow.

## Features
- Crop recommendation engine
- Crop suitability evaluation
- User authentication with JWT
- Recommendation history dashboard
- Responsive UI
- Seeded crop profiles and sample data

## Project structure
- backend/: FastAPI API and recommendation engine
- frontend/: Vite + React web app
- database/: SQL seed data
- docs/: Additional documentation

## Backend setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```

## Test
```bash
cd backend
pytest -q
```

## API overview
- POST /auth/register
- POST /auth/login
- POST /recommend
- POST /evaluate
- GET /dashboard
- GET /health

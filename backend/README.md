# Deepfake Detection API

FastAPI backend for image, video, and audio deepfake detection.

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: DATABASE_URL, MONGODB_URL, SECRET_KEY
```

## Database

- **PostgreSQL**: Create DB and set `DATABASE_URL`. Tables (e.g. `users`) are created on startup.
- **MongoDB**: Set `MONGODB_URL` and `MONGODB_DB`. Used for detection results and history.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register (email, password, full_name) |
| POST | `/api/auth/login` | Login → JWT |
| GET | `/api/auth/me` | Current user (Bearer token) |
| POST | `/api/detect/image` | Upload image → detection result |
| POST | `/api/detect/video` | Upload video → detection result |
| POST | `/api/detect/audio` | Upload audio → detection result |
| GET | `/api/results/history` | List user's detection history |
| GET | `/api/results/report/{id}` | Get one report |
| GET | `/api/results/report/{id}/download` | Download forensic JSON |
| GET | `/api/admin/analytics` | Admin: usage stats |
| GET | `/api/admin/users` | Admin: user list (stub) |

## Detection Response (example)

```json
{
  "success": true,
  "media_type": "image",
  "result": {
    "label": "real",
    "confidence": 0.87,
    "confidence_real": 0.87,
    "confidence_fake": 0.13,
    "heatmap_url": null,
    "report_id": "uuid"
  }
}
```

Video responses include `frame_scores` and `timeline` for temporal visualization.

## Environment Variables

See `.env.example`. Key ones: `SECRET_KEY`, `DATABASE_URL`, `MONGODB_URL`, `MONGODB_DB`, `MAX_FILE_SIZE_MB`.

# AI-Powered Deepfake Detection System

Web-based platform that analyzes **images**, **videos**, and **audio** to detect deepfakes using CNN, RNN, and Transformer-based models. Provides confidence scores, visual explanations, and forensic reports.

## Architecture

```
User → Frontend (Next.js) → Backend (FastAPI) → AI Models → MongoDB / PostgreSQL → Result
```

## Tech Stack

| Layer        | Technology                    |
|-------------|-------------------------------|
| Frontend    | Next.js 14, Tailwind CSS      |
| Backend     | FastAPI (AI inference + REST) |
| Auth        | JWT (FastAPI)                 |
| AI          | PyTorch, OpenCV, Librosa      |
| Databases   | MongoDB (results), PostgreSQL (users) |
| Deployment  | Docker                        |

## Quick Start

### Prerequisites

- Node.js 18+, Python 3.10+, Docker (optional)

### Backend (FastAPI + AI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
# Set .env (see backend/.env.example)
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### With Docker

```bash
docker-compose up -d
```

## Core Features

- **Image**: CNN (EfficientNet/ResNet), face extraction, heatmap, confidence %
- **Video**: Frame extraction, CNN + LSTM, temporal inconsistency, timeline
- **Audio**: Spectrogram CNN, voice-clone / synthesis detection
- **Dashboard**: Upload, results, confidence meter, history, forensic report download
- **Roles**: Normal user (upload, history, reports), Admin (users, analytics, model retrain)

## Security

- JWT authentication, file encryption, auto-delete after analysis, rate limiting

## Docs

- [API Documentation](backend/README.md#api)
- [SRS](docs/SRS.md) (outline in repo)

## License

MIT

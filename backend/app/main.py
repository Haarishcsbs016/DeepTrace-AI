from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.routers import auth, detect, results, admin
from app.db.mongodb import connect_mongo, close_mongo
from app.db.postgres import init_pg

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_mongo()
    await init_pg()
    yield
    await close_mongo()


app = FastAPI(
    title="Deepfake Detection API",
    description="AI-powered detection for images, video, and audio",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(detect.router, prefix="/api/detect", tags=["Detection"])
app.include_router(results.router, prefix="/api/results", tags=["Results"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"service": "Deepfake Detection API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}

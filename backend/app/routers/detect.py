import uuid
import aiofiles
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.auth.deps import get_current_user
from app.models.user import User
from app.db.mongodb import get_db
from app.config import get_settings
from app.services.detection import run_image_detection, run_video_detection, run_audio_detection
from app.schemas.detect import (
    ImageDetectionResponse,
    VideoDetectionResponse,
    AudioDetectionResponse,
    DetectionResult,
)

router = APIRouter()
settings = get_settings()
UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_VIDEO = {"video/mp4", "video/webm", "video/avi"}
ALLOWED_AUDIO = {"audio/wav", "audio/mpeg", "audio/mp3", "audio/webm"}


def get_media_type(content_type: str) -> str | None:
    if content_type in ALLOWED_IMAGE:
        return "image"
    if content_type in ALLOWED_VIDEO:
        return "video"
    if content_type in ALLOWED_AUDIO:
        return "audio"
    return None


@router.post("/image", response_model=ImageDetectionResponse)
async def detect_image(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_IMAGE:
        raise HTTPException(400, "Invalid file type. Use JPEG, PNG, or WebP.")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename or 'image.jpg'}"
    try:
        async with aiofiles.open(path, "wb") as f:
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(400, f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)")
            await f.write(content)
        result = await run_image_detection(str(path))
    finally:
        if path.exists():
            path.unlink(missing_ok=True)
    report_id = str(uuid.uuid4())
    await store_result(get_db(), user.id, "image", report_id, result)
    result.report_id = report_id
    return ImageDetectionResponse(result=result)


@router.post("/video", response_model=VideoDetectionResponse)
async def detect_video(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_VIDEO:
        raise HTTPException(400, "Invalid file type. Use MP4, WebM, or AVI.")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename or 'video.mp4'}"
    try:
        async with aiofiles.open(path, "wb") as f:
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(400, f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)")
            await f.write(content)
        result = await run_video_detection(str(path))
    finally:
        if path.exists():
            path.unlink(missing_ok=True)
    report_id = str(uuid.uuid4())
    await store_result(get_db(), user.id, "video", report_id, result)
    result.report_id = report_id
    return VideoDetectionResponse(result=result)


@router.post("/audio", response_model=AudioDetectionResponse)
async def detect_audio(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_AUDIO:
        raise HTTPException(400, "Invalid file type. Use WAV, MP3, or WebM audio.")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename or 'audio.wav'}"
    try:
        async with aiofiles.open(path, "wb") as f:
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(400, f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)")
            await f.write(content)
        result = await run_audio_detection(str(path))
    finally:
        if path.exists():
            path.unlink(missing_ok=True)
    report_id = str(uuid.uuid4())
    await store_result(get_db(), user.id, "audio", report_id, result)
    result.report_id = report_id
    return AudioDetectionResponse(result=result)


async def store_result(db, user_id: int, media_type: str, report_id: str, result: DetectionResult):
    if not db:
        return
    await db.results.insert_one({
        "report_id": report_id,
        "user_id": user_id,
        "media_type": media_type,
        "label": result.label,
        "confidence": result.confidence,
        "confidence_real": result.confidence_real,
        "confidence_fake": result.confidence_fake,
        "frame_scores": result.frame_scores,
        "timeline": result.timeline,
    })

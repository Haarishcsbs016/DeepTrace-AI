import asyncio
from app.schemas.detect import DetectionResult
from app.ml.image_detector import detect_image as ml_detect_image
from app.ml.video_detector import detect_video as ml_detect_video
from app.ml.audio_detector import detect_audio as ml_detect_audio


def _run_sync(fn, *args, **kwargs):
    return asyncio.to_thread(fn, *args, **kwargs)


async def run_image_detection(path: str) -> DetectionResult:
    return await _run_sync(ml_detect_image, path)


async def run_video_detection(path: str) -> DetectionResult:
    return await _run_sync(ml_detect_video, path)


async def run_audio_detection(path: str) -> DetectionResult:
    return await _run_sync(ml_detect_audio, path)

from pydantic import BaseModel
from typing import Literal


class DetectionResult(BaseModel):
    label: Literal["real", "fake"]
    confidence: float  # 0-1
    confidence_real: float | None = None
    confidence_fake: float | None = None
    heatmap_url: str | None = None
    manipulated_regions: list[dict] | None = None
    frame_scores: list[float] | None = None  # video
    timeline: list[dict] | None = None
    report_id: str | None = None


class ImageDetectionResponse(BaseModel):
    success: bool = True
    media_type: Literal["image"] = "image"
    result: DetectionResult


class VideoDetectionResponse(BaseModel):
    success: bool = True
    media_type: Literal["video"] = "video"
    result: DetectionResult


class AudioDetectionResponse(BaseModel):
    success: bool = True
    media_type: Literal["audio"] = "audio"
    result: DetectionResult

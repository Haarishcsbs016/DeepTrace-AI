"""
Video deepfake detection: frame extraction, CNN + temporal (LSTM) analysis.
Returns frame-level scores and aggregated result.
"""
import numpy as np
from pathlib import Path

from app.schemas.detect import DetectionResult

_cv2 = None


def _imports():
    global _cv2
    if _cv2 is None:
        import cv2 as _cv2
    return _cv2


def _extract_frames(video_path: str, max_frames: int = 30) -> list[np.ndarray]:
    cv2 = _imports()
    cap = cv2.VideoCapture(video_path)
    frames = []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        cap.release()
        return []
    step = max(1, total // max_frames)
    i = 0
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if i % step == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224))
            frames.append(frame)
        i += 1
    cap.release()
    return frames


def _frame_scores(frames: list[np.ndarray]) -> list[float]:
    """Stub: per-frame fake probability. Replace with real CNN+LSTM."""
    if not frames:
        return [0.5]
    # Demo: slight variation per frame
    base = 0.4 + 0.1 * (np.mean(frames[0]) / 255.0)
    return [float(np.clip(base + (i % 5) * 0.02, 0, 1)) for i in range(len(frames))]


def detect_video(video_path: str) -> DetectionResult:
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    frames = _extract_frames(video_path)
    if not frames:
        return DetectionResult(
            label="real",
            confidence=0.5,
            confidence_real=0.5,
            confidence_fake=0.5,
            frame_scores=[],
            timeline=[],
        )
    scores = _frame_scores(frames)
    prob_fake = float(np.mean(scores))
    prob_real = 1.0 - prob_fake
    label = "real" if prob_real >= prob_fake else "fake"
    confidence = max(prob_real, prob_fake)
    timeline = [{"frame": i, "score": s, "anomaly": s > 0.6} for i, s in enumerate(scores)]
    return DetectionResult(
        label=label,
        confidence=confidence,
        confidence_real=prob_real,
        confidence_fake=prob_fake,
        frame_scores=scores,
        timeline=timeline,
    )

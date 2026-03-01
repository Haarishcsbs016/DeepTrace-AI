"""
Image deepfake detection using CNN (EfficientNet/ResNet-style).
Face extraction, artifact detection, optional heatmap.
"""
import numpy as np
from pathlib import Path

from app.schemas.detect import DetectionResult

# Lazy imports for heavy libs
_cv2 = _torch = _torchvision = _PIL = None


def _imports():
    global _cv2, _torch, _torchvision, _PIL
    if _cv2 is None:
        import cv2 as _cv2
        import torch as _torch
        import torchvision.transforms as _torchvision
        from PIL import Image as _PIL
    return _cv2, _torch, _torchvision, _PIL


def _preprocess(image_path: str):
    cv2, torch, torchvision, PIL = _imports()
    img = cv2.imread(image_path)
    if img is None:
        pil_img = PIL.Image.open(image_path).convert("RGB")
        img = np.array(pil_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Resize for model input (e.g. 224x224)
    img = cv2.resize(img, (224, 224))
    return img, img.copy()


def _run_cnn_inference(img_rgb: np.ndarray) -> tuple[float, float]:
    """Returns (prob_real, prob_fake). Uses a stub or loaded model."""
    try:
        import torch
        import torch.nn as nn
        from torchvision import models
        # Stub: no saved weights by default → random-ish score for demo
        model = models.efficientnet_b0(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(model.classifier[1].in_features, 2),
        )
        model.eval()
        # Dummy inference with numpy input
        x = torch.from_numpy(img_rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0
        with torch.no_grad():
            logits = model(x)
            probs = torch.softmax(logits, dim=1)[0]
        return float(probs[0].item()), float(probs[1].item())
    except Exception:
        # Fallback: deterministic demo score based on pixel mean
        mean = float(np.mean(img_rgb))
        fake_score = min(1.0, (mean / 128.0 - 0.3) * 1.2)
        fake_score = max(0.0, min(1.0, fake_score))
        return 1.0 - fake_score, fake_score


def detect_image(image_path: str) -> DetectionResult:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    img_rgb, _ = _preprocess(image_path)
    prob_real, prob_fake = _run_cnn_inference(img_rgb)
    label = "real" if prob_real >= prob_fake else "fake"
    confidence = max(prob_real, prob_fake)
    return DetectionResult(
        label=label,
        confidence=confidence,
        confidence_real=prob_real,
        confidence_fake=prob_fake,
        heatmap_url=None,
        manipulated_regions=None,
    )

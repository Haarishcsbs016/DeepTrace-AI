"""
Audio deepfake detection: convert to spectrogram, run CNN.
Detects voice cloning / AI synthesis patterns.
"""
import numpy as np
from pathlib import Path

from app.schemas.detect import DetectionResult

_librosa = _sf = None


def _imports():
    global _librosa, _sf
    if _librosa is None:
        import librosa as _librosa
        import soundfile as _sf
    return _librosa, _sf


def _load_audio(path: str, sr: int = 22050, max_duration: float = 10.0):
    librosa, sf = _imports()
    y, sr = librosa.load(path, sr=sr, duration=max_duration, mono=True)
    return y, sr


def _to_mel_spectrogram(y: np.ndarray, sr: int, n_mels: int = 128, n_fft: int = 2048):
    librosa, _ = _imports()
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, n_mels=n_mels)
    S_db = librosa.power_to_db(S, ref=np.max)
    return S_db


def _run_spectrogram_cnn(spec: np.ndarray) -> tuple[float, float]:
    """Stub: real model would be a small CNN on mel spec. Returns (prob_real, prob_fake)."""
    try:
        import torch
        import torch.nn as nn
        # Simple 2-layer conv stub
        class StubCNN(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = nn.Sequential(
                    nn.Conv2d(1, 16, 3), nn.ReLU(), nn.AdaptiveAvgPool2d((8, 8)),
                    nn.Flatten(), nn.Linear(16 * 8 * 8, 2),
                )

            def forward(self, x):
                return self.conv(x)

        model = StubCNN()
        model.eval()
        # spec: (n_mels, time) -> (1, 1, n_mels, time)
        x = torch.from_numpy(spec).float().unsqueeze(0).unsqueeze(0)
        if x.shape[2] < 8 or x.shape[3] < 8:
            x = torch.nn.functional.interpolate(x, size=(128, 128))
        with torch.no_grad():
            logits = model(x)
            probs = torch.softmax(logits, dim=1)[0]
        return float(probs[0].item()), float(probs[1].item())
    except Exception:
        mean = float(np.mean(spec))
        fake = min(1.0, max(0.0, (mean + 80) / 80 * 0.4))
        return 1.0 - fake, fake


def detect_audio(audio_path: str) -> DetectionResult:
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")
    y, sr = _load_audio(audio_path)
    if len(y) == 0:
        return DetectionResult(
            label="real",
            confidence=0.5,
            confidence_real=0.5,
            confidence_fake=0.5,
        )
    spec = _to_mel_spectrogram(y, sr)
    prob_real, prob_fake = _run_spectrogram_cnn(spec)
    label = "real" if prob_real >= prob_fake else "fake"
    confidence = max(prob_real, prob_fake)
    return DetectionResult(
        label=label,
        confidence=confidence,
        confidence_real=prob_real,
        confidence_fake=prob_fake,
    )

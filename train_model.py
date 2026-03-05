"""
Dataset preparation and training script for the deepfake detection model.

RECOMMENDED DATASETS:
=====================

1. **140k Real and Fake Faces** (Kaggle)
   - URL: https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces
   - Contains 70k real faces from FFHQ and 70k fake faces from StyleGAN
   - Download and extract to: datasets/140k-real-fake-faces/

2. **Deepfake Detection Challenge** (Kaggle/DFDC)
   - URL: https://www.kaggle.com/c/deepfake-detection-challenge/data
   - Large-scale video dataset with real and manipulated videos
   - Extract frames for image training

3. **FaceForensics++**
   - URL: https://github.com/ondyari/FaceForensics
   - Academic dataset with various manipulation types
   - Requires request for access

4. **CelebDF** (Celebrity DeepFake)
   - URL: https://github.com/yuezunli/celeb-deepfakeforensics
   - High-quality deepfake videos of celebrities

5. **AI-Generated Images Dataset**
   - DALL-E, Midjourney, Stable Diffusion generated images
   - Collect from various sources or generate yourself

DIRECTORY STRUCTURE:
====================
datasets/
├── real/           # Real images (photos, camera images)
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
└── fake/           # Fake/AI-generated images
    ├── fake1.jpg
    ├── fake2.png
    └── ...

USAGE:
======
    python train_model.py --real-dir datasets/real --fake-dir datasets/fake

Or from Python:
    from train_model import train_from_directories
    accuracy = train_from_directories("datasets/real", "datasets/fake")
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Tuple
import random

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def collect_image_paths(directory: str, extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.webp')) -> List[str]:
    """Collect all image paths from a directory recursively."""
    paths = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    for ext in extensions:
        paths.extend([str(p) for p in dir_path.rglob(f"*{ext}")])
        paths.extend([str(p) for p in dir_path.rglob(f"*{ext.upper()}")])
    
    return paths


def train_from_directories(
    real_dir: str,
    fake_dir: str,
    max_images_per_class: int = 5000,
    test_split: float = 0.2,
) -> dict:
    """
    Train the model from directories of real and fake images.
    
    Args:
        real_dir: Directory containing real images
        fake_dir: Directory containing fake/AI-generated images
        max_images_per_class: Maximum images to use per class
        test_split: Fraction of data to use for testing
    
    Returns:
        Dictionary with training results
    """
    import numpy as np
    import cv2
    from app.ml.feature_extractor import extract_all_features
    from app.ml.rf_model import get_model
    
    logger.info("Collecting image paths...")
    real_paths = collect_image_paths(real_dir)
    fake_paths = collect_image_paths(fake_dir)
    
    logger.info(f"Found {len(real_paths)} real images")
    logger.info(f"Found {len(fake_paths)} fake images")
    
    if len(real_paths) < 10 or len(fake_paths) < 10:
        raise ValueError("Need at least 10 images of each type")
    
    # Limit and shuffle
    random.shuffle(real_paths)
    random.shuffle(fake_paths)
    real_paths = real_paths[:max_images_per_class]
    fake_paths = fake_paths[:max_images_per_class]
    
    # Extract features
    logger.info("Extracting features from images...")
    X_list = []
    y_list = []
    errors = 0
    
    for i, path in enumerate(real_paths):
        try:
            img = cv2.imread(path)
            if img is not None:
                img = cv2.resize(img, (512, 512))
                features = extract_all_features(img)
                X_list.append(features)
                y_list.append(0)  # Real
            else:
                errors += 1
        except Exception as e:
            errors += 1
            logger.debug(f"Error processing {path}: {e}")
        
        if (i + 1) % 100 == 0:
            logger.info(f"Processed {i + 1}/{len(real_paths)} real images")
    
    for i, path in enumerate(fake_paths):
        try:
            img = cv2.imread(path)
            if img is not None:
                img = cv2.resize(img, (512, 512))
                features = extract_all_features(img)
                X_list.append(features)
                y_list.append(1)  # Fake
            else:
                errors += 1
        except Exception as e:
            errors += 1
            logger.debug(f"Error processing {path}: {e}")
        
        if (i + 1) % 100 == 0:
            logger.info(f"Processed {i + 1}/{len(fake_paths)} fake images")
    
    logger.info(f"Total images processed: {len(X_list)} ({errors} errors)")
    
    X = np.array(X_list)
    y = np.array(y_list)
    
    # Split into train and test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_split, random_state=42, stratify=y
    )
    
    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    
    # Train model
    logger.info("Training Random Forest model...")
    model = get_model()
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    
    model.model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.scaler = StandardScaler()
    
    X_train_scaled = model.scaler.fit_transform(X_train)
    X_test_scaled = model.scaler.transform(X_test)
    
    model.model.fit(X_train_scaled, y_train)
    model.is_trained = True
    
    # Evaluate
    y_pred = model.model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Accuracy: {accuracy:.2%}")
    logger.info(f"{'='*50}")
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
    logger.info("\nConfusion Matrix:")
    logger.info(confusion_matrix(y_test, y_pred))
    
    # Save model
    model.save_model()
    logger.info("Model saved successfully!")
    
    # Feature importance
    importance = model.model.feature_importances_
    top_indices = importance.argsort()[::-1][:10]
    logger.info("\nTop 10 Most Important Features:")
    for i, idx in enumerate(top_indices):
        logger.info(f"  {i+1}. Feature {idx}: {importance[idx]:.4f}")
    
    return {
        "accuracy": accuracy,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "real_images": len(real_paths) - errors // 2,
        "fake_images": len(fake_paths) - errors // 2,
    }


def download_sample_dataset():
    """Download a small sample dataset for testing."""
    logger.info("To download datasets, please visit:")
    logger.info("1. https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces")
    logger.info("2. https://www.kaggle.com/c/deepfake-detection-challenge/data")
    logger.info("")
    logger.info("After downloading, organize images into:")
    logger.info("  datasets/real/ - for real images")
    logger.info("  datasets/fake/ - for fake/AI-generated images")
    logger.info("")
    logger.info("Then run: python train_model.py --real-dir datasets/real --fake-dir datasets/fake")


def main():
    parser = argparse.ArgumentParser(description="Train deepfake detection model")
    parser.add_argument("--real-dir", type=str, help="Directory with real images")
    parser.add_argument("--fake-dir", type=str, help="Directory with fake images")
    parser.add_argument("--max-images", type=int, default=5000, help="Max images per class")
    parser.add_argument("--download", action="store_true", help="Show download instructions")
    
    args = parser.parse_args()
    
    if args.download:
        download_sample_dataset()
        return
    
    if not args.real_dir or not args.fake_dir:
        parser.print_help()
        print("\nExample usage:")
        print("  python train_model.py --real-dir datasets/real --fake-dir datasets/fake")
        print("\nTo see dataset download instructions:")
        print("  python train_model.py --download")
        return
    
    results = train_from_directories(
        args.real_dir,
        args.fake_dir,
        max_images_per_class=args.max_images,
    )
    
    print(f"\nTraining complete!")
    print(f"Accuracy: {results['accuracy']:.2%}")
    print(f"Training samples: {results['train_samples']}")
    print(f"Test samples: {results['test_samples']}")


if __name__ == "__main__":
    main()

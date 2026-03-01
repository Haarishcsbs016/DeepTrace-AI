# Software Requirements Specification (SRS)  
# AI-Powered Deepfake Detection System

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for a web-based **AI Deepfake Detection System** that analyzes images, video, and audio to determine whether content is real or synthetically manipulated.

### 1.2 Scope
- **In scope**: Web application for uploading media, running AI-based detection, viewing results (confidence scores, visualizations), user authentication, history, forensic report download, and admin analytics.
- **Out of scope**: Training models from scratch in the product (pre-trained or fine-tunable models only), mobile native apps, real-time streaming analysis in v1.

### 1.3 Definitions
- **Deepfake**: Synthetically generated or altered media (e.g., via DeepFaceLab, FaceSwap, D-ID, voice cloning).
- **Confidence score**: Probability (0–100%) that the media is real or fake.
- **Forensic report**: JSON (or PDF) output containing verdict, scores, and metadata for a single detection.

---

## 2. Overall Description

### 2.1 Product Perspective
- **User** → **Frontend (Next.js)** → **Backend API (FastAPI)** → **AI models** → **Databases** → **Result**.
- External systems may integrate via REST API (e.g., media companies, moderation pipelines).

### 2.2 User Classes
- **Normal user**: Register, login, upload media, view results, download reports, view history.
- **Admin**: All of the above plus user management, usage analytics, and (future) model retraining/monitoring.

### 2.3 Operating Environment
- Browsers: Chrome, Firefox, Safari, Edge (latest).
- Server: Linux/Windows, Docker; Python 3.10+, Node 18+ for tooling if used.
- Databases: PostgreSQL (user accounts, logs), MongoDB (detection results, history).

### 2.4 Constraints
- File size limits (e.g., max 100 MB per file).
- Rate limiting per user to avoid abuse.
- Media deleted after analysis (configurable) for privacy.

---

## 3. System Features and Requirements

### 3.1 Image Deepfake Detection
- **FR-1.1** System shall accept image uploads (JPEG, PNG, WebP).
- **FR-1.2** System shall run CNN-based inference (e.g., ResNet/EfficientNet) for binary classification (real/fake).
- **FR-1.3** System shall return a verdict (real/fake), confidence percentage, and optional heatmap/manipulated regions.
- **FR-1.4** System shall support face extraction and artifact detection in the pipeline.

### 3.2 Video Deepfake Detection
- **FR-2.1** System shall accept video uploads (e.g., MP4, WebM, AVI).
- **FR-2.2** System shall extract frames and run per-frame and/or temporal (e.g., LSTM) analysis.
- **FR-2.3** System shall return an aggregate verdict and optional frame-by-frame anomaly scores and timeline visualization.

### 3.3 Audio Deepfake Detection
- **FR-3.1** System shall accept audio uploads (WAV, MP3, etc.).
- **FR-3.2** System shall convert audio to spectrogram and run CNN-based analysis.
- **FR-3.3** System shall return a verdict and confidence for synthetic voice / AI speech detection.

### 3.4 User Management and Security
- **FR-4.1** System shall provide user registration and login (email + password).
- **FR-4.2** System shall use JWT for session management and API authentication.
- **FR-4.3** System shall enforce role-based access (user vs admin).
- **FR-4.4** System shall support rate limiting and secure file handling (validation, size limits).

### 3.5 Results and Reporting
- **FR-5.1** System shall store detection results in a database (MongoDB) linked to the user.
- **FR-5.2** System shall provide a history view and forensic report download (e.g., JSON).
- **FR-5.3** Admin shall be able to view usage analytics (e.g., total detections, by type).

---

## 4. External Interface Requirements

### 4.1 User Interface
- Minimal, professional UI with dark theme (cybersecurity style).
- Upload area (drag-and-drop), result panel with confidence meter (e.g., circular progress), detection timeline for video, history table.

### 4.2 API
- REST API documented via OpenAPI (FastAPI `/docs`).
- Endpoints: auth (register, login, me), detect (image, video, audio), results (history, report, download), admin (analytics).

### 4.3 Databases
- **PostgreSQL**: Users, roles, audit logs.
- **MongoDB**: Detection results (report_id, user_id, media_type, label, confidence, frame_scores, timeline, etc.).

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Response time for detection: target &lt; 30 s for typical image; &lt; 2 min for short video/audio depending on length and hardware.
- Metrics: accuracy, precision, recall, F1, ROC where applicable.

### 5.2 Security
- Passwords hashed (e.g., bcrypt); JWT with configurable expiry; file type/size validation; optional auto-delete of uploaded media after analysis.

### 5.3 Scalability
- Stateless API; database and model inference can be scaled (e.g., separate worker for heavy ML).

---

## 6. Deliverables

- Working web application (frontend + backend).
- API documentation (OpenAPI/Swagger).
- This SRS document.
- Model accuracy report (when models are fixed/trained).
- Deployment instructions (e.g., Docker, README).

---

*Document version: 1.0 | AI-Powered Deepfake Detection System*

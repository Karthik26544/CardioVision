# CardioVision — Interactive 3D Cardiovascular Risk Visualization

**Track A:** Cardiovascular Risk Visualization & Prediction  
**Event:** Multimodal AI Hackathon 2026  
**Organizers:** KamandPrompt (IIT Mandi) × Augli.ai × PurpleRain Tech × LDV Labs  
**Team:** CardioVision (Solo)  

**Demo Video:** [Watch Demo Video on YouTube](https://youtu.be/jvRckP1kZO0)

---

## Overview

CardioVision is a web-based clinical decision-support prototype that converts patient physiological data (demographics, vitals, lab values, ECG features) into **real-time, vessel-specific 3D anatomical risk maps**.

It predicts:
- Overall Coronary Artery Disease (CAD) risk
- Stenosis probability for the three major coronary arteries:
  - **LAD** (Left Anterior Descending)
  - **LCX** (Left Circumflex)
  - **RCA** (Right Coronary Artery)

Predictions are dynamically color-coded on an interactive 3D heart (Green = Low Risk, Red = High Risk) and explained via SHAP-style feature attribution for clinical interpretability.

---

## Key Features

- Multi-vessel Random Forest classification (zero target leakage)
- Real-time WebGL 3D anatomical heart visualization (Three.js)
- Dynamic LAD / LCX / RCA vessel highlighting + pulse emission
- Click-to-inspect vessel details (Raycasting)
- Clinical Interpretability dashboard (top contributing physiological factors)
- Java Spring Boot orchestration layer
- Python FastAPI ML microservice
- Mandatory clinical safety disclaimer

---

## Tech Stack

| Layer              | Technology                                      |
|--------------------|-------------------------------------------------|
| Frontend           | HTML5, CSS3, Vanilla JS, Three.js (WebGL)      |
| Backend            | Java 17, Spring Boot 3                         |
| ML Engine          | Python 3.11, FastAPI, Scikit-learn, Joblib     |
| 3D Assets          | Anatomical `.glb` heart model + procedural vessels |
| Dataset            | Z-Alizadeh Sani (UCI / Kaggle)                 |

---

## Project Structure

```text
Cardio_Vision/
├── ml_backend/                 # Python ML + FastAPI
│   ├── app.py
│   ├── train.py
│   ├── model_*.pkl
│   ├── feature_names.pkl
│   ├── imputer.pkl
│   └── Z-Alizadeh_Sani.xlsx
├── java_backend/               # Spring Boot 3 REST API
│   ├── src/main/java/...
│   └── pom.xml
├── frontend/                   # 3D Web UI
│   ├── index.html
│   └── human_heart_realistic_anatomical_model.glb
└── README.md
```

## How to Run Locally

### Prerequisites

- Python 3.11+
- Java 17+
- Maven (or use the included `mvnw`)

### 1. Start Python ML Engine (Port 8000)

```bash
cd ml_backend
py -m pip install pandas scikit-learn joblib fastapi uvicorn pydantic openpyxl
py train.py   # only needed once
py -m uvicorn app:app --reload --port 8000
```

### 2. Start Java Spring Boot Backend (Port 8080)

```bash
cd java_backend
.\mvnw spring-boot:run
```

### 3. Launch Frontend (Port 3000)

```bash
cd frontend
py -m http.server 3000
```

Open in browser: [http://localhost:3000](http://localhost:3000)

## Architecture Flow

```text
Browser (Three.js UI)
        │  POST /api/predict
        ▼
Java Spring Boot (Port 8080)
        │  RestTemplate → {"features": {...}}
        ▼
Python FastAPI (Port 8000)
        │  Random Forest models + feature importances
        ▼
JSON Response → Color mapping + SHAP factors → 3D vessel update
```

## AI Tools & Assistance Disclosure

In accordance with hackathon guidelines, AI coding assistants were used for rapid prototyping and boilerplate generation:

- **Cursor AI & ChatGPT:** Used for generating starter boilerplate (Spring Boot controllers/services, Three.js scene setup, FastAPI routes, documentation formatting). All generated code was manually reviewed, edited, integrated, and customized.
- **ElevenLabs:** Used to generate clear professional voiceover for the demonstration video.

Core design decisions (anti-leakage feature dropping, multi-model architecture, vessel mapping logic, evaluation metrics, and system integration) were made and verified by the developer. The author can fully explain every part of the system.

## Clinical Safety Disclaimer

> **CardioVision is intended strictly for educational and clinical decision-support purposes only.**
> It is not a substitute for formal diagnostic imaging, cardiac catheterization, or professional medical judgment.

## Evaluation Alignment

| Criteria | Weight | How CardioVision Addresses It |
|---|---|---|
| Predictive Performance | 30% | 4 Random Forest models + proper metrics + no leakage |
| 3D Visualization | 25% | Anatomical heart + dynamic LAD/LCX/RCA coloring + rotate/zoom/click |
| Clinical Interpretability | 20% | Feature importance / SHAP-style attribution bars |
| System Integration | 15% | Seamless Java ↔ Python ↔ Frontend pipeline |
| Technical Implementation | 10% | Clean architecture, public dataset, reproducible |

## Author

**Team CardioVision** (Solo Developer)
B.Tech 2nd Year | Learning Java Backend + Multimodal AI

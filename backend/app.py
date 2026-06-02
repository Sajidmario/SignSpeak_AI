from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import torch
import json
import numpy as np
import base64
import io
from PIL import Image
import mediapipe as mp

from model import SignLanguageModel
from utils import extract_keypoints

# =========================
# FastAPI Setup
# =========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load Model
# =========================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("label_map.json", "r") as f:
    label_map = {int(k): v for k, v in json.load(f).items()}

feat_mean = np.load("feat_mean.npy")
feat_std = np.load("feat_std.npy")

print("Mean shape:", feat_mean.shape)
print("Std shape:", feat_std.shape)

NUM_CLASSES = len(label_map)

model = SignLanguageModel(
    input_size=225,
    cnn_hidden=256,
    lstm_hidden=256,
    num_layers=2,
    num_classes=NUM_CLASSES,
    dropout=0.5
).to(DEVICE)

checkpoint = torch.load(
    "isl_finetuned_v6.pth",
    map_location=DEVICE
)

print("Checkpoint classes:", checkpoint.get("num_classes", "Unknown"))
print("Label map classes:", NUM_CLASSES)
print("Stage:", checkpoint.get("stage", "Unknown"))
print("Val Acc:", checkpoint.get("val_acc", "Unknown"))

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()

print(f"✅ Model Loaded ({NUM_CLASSES} classes)")

# =========================
# Request Schema
# =========================

class PredictRequest(BaseModel):
    frames: list[str]

# =========================
# MediaPipe
# =========================

mp_holistic = mp.solutions.holistic

# =========================
# Routes
# =========================

@app.get("/")
def root():
    return {
        "status": "working",
        "model_loaded": True
    }

@app.get("/model-info")
def model_info():
    return {
        "classes": NUM_CLASSES,
        "device": str(DEVICE)
    }

@app.post("/predict")
def predict(request: PredictRequest):

    if len(request.frames) != 30:
        return {
            "error": f"Expected 30 frames, got {len(request.frames)}"
        }

    sequence = []

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        for frame_data in request.frames:

            if "," in frame_data:
                frame_data = frame_data.split(",")[1]

            image_bytes = base64.b64decode(frame_data)

            image = Image.open(
                io.BytesIO(image_bytes)
            ).convert("RGB")

            image_np = np.array(image)

            results = holistic.process(image_np)

            keypoints = extract_keypoints(results)

            sequence.append(keypoints)

    # ADD THE NEW CODE HERE
    sequence = np.array(sequence, dtype=np.float32)

    print("Sequence shape:", sequence.shape)

    if sequence.shape != (30, 225):
        return {
            "error": f"Expected sequence shape (30,225), got {sequence.shape}"
        }

    sequence = (sequence - feat_mean) / feat_std

    print(
        "Normalized stats:",
        float(sequence.mean()),
        float(sequence.std())
    )

    input_tensor = (
        torch.tensor(sequence)
        .unsqueeze(0)
        .to(DEVICE)
    )

    with torch.no_grad():
        probs = torch.softmax(
            model(input_tensor),
            dim=1
        )[0]

    top_prob, top_idx = probs.max(dim=0)

    prediction = label_map[int(top_idx.item())]

    confidence = float(top_prob.item() * 100)

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2)
    }
import os
import json
import cv2
import torch
import torch.nn as nn
import numpy as np
import mediapipe as mp
import time

# 1. Config
BASE_DIR = r'C:\Users\LENOVO\OneDrive\Documents\Projects\MyNotebooks\Sign Language'
FINETUNED_PATH = os.path.join(BASE_DIR, 'isl_finetuned_v6.pth')
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SEQUENCE_LENGTH = 30
NUM_FEATURES = 225
HIDDEN_SIZE = 256
NUM_LAYERS = 2

class CNNFeatureExtractor(nn.Module):
    def __init__(self, in_features=225, out_features=256):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv1d(in_features, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128), nn.GELU(), nn.Dropout(0.2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(128, out_features, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_features), nn.GELU(), nn.Dropout(0.2)
        )
        self.conv3 = nn.Sequential(
            nn.Conv1d(out_features, out_features, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_features), nn.GELU(), nn.Dropout(0.2)
        )

    def forward(self, x):
        x = x.transpose(1, 2)
        x = self.conv1(x)
        x = self.conv2(x)
        residual = x
        x = self.conv3(x) + residual
        return x.transpose(1, 2)

class TemporalTransformerBlock(nn.Module):
    def __init__(self, d_model=512, nhead=8, dim_ff=1024, dropout=0.3):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, dim_ff), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(dim_ff, d_model), nn.Dropout(dropout),
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        attn_out, _ = self.self_attn(x, x, x)
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ff(x))
        return x

class AttentionLayer(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attention = nn.Linear(hidden_size, 1)

    def forward(self, lstm_out):
        weights = torch.softmax(self.attention(lstm_out), dim=1)
        context = (weights * lstm_out).sum(dim=1)
        return context, weights

class SignLanguageModel(nn.Module):
    def __init__(self, input_size=225, cnn_hidden=256, lstm_hidden=256, num_layers=2, num_classes=255, dropout=0.5):
        super().__init__()
        self.cnn = CNNFeatureExtractor(input_size, cnn_hidden)
        self.lstm = nn.LSTM(
            input_size=cnn_hidden, hidden_size=lstm_hidden, num_layers=num_layers,
            batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0.0
        )
        self.transformer = TemporalTransformerBlock(d_model=lstm_hidden * 2, dropout=0.3)
        self.attention = AttentionLayer(lstm_hidden * 2)
        
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(lstm_hidden * 2)
        self.fc = nn.Linear(lstm_hidden * 2, num_classes)

    def forward(self, x):
        x = self.cnn(x)                     
        x, _ = self.lstm(x)                 
        x = self.transformer(x)             
        context, _ = self.attention(x)      
        
        context = self.norm(context)
        context = self.dropout(context)
        return self.fc(context)
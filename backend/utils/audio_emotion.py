import librosa
import numpy as np
import os

def extract_features(audio_path):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Extract basic waveform features
        rms = np.mean(librosa.feature.rms(y=y))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

        return {
            "rms": float(rms),
            "zcr": float(zcr),
            "centroid": float(centroid)
        }

    except Exception as e:
        print("AUDIO FEATURE ERROR:", e)
        return None


def detect_emotion_from_audio(features):
    if not features:
        return {
            "emotion": "neutral",
            "stress_level": "low",
            "burnout_score": 20
        }

    rms = features["rms"]
    zcr = features["zcr"]

    # 🚨 HEURISTIC LOGIC (WAVEFORM ANALYSIS)
    
    # 1. High Energy + High Frequency Change = Stress/Agitation
    if rms > 0.05 and zcr > 0.1:
        return {
            "emotion": "stress",
            "stress_level": "high",
            "burnout_score": 80
        }

    # 2. Very Low Energy = Fatigue/Exhaustion
    elif rms < 0.02:
        return {
            "emotion": "fatigue",
            "stress_level": "medium",
            "burnout_score": 60
        }

    # 3. Baseline = Neutral
    else:
        return {
            "emotion": "neutral",
            "stress_level": "low",
            "burnout_score": 30
        }

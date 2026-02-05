import requests

HF_API_URL = "https://abhinavdread-spam-detection.hf.space/predict"
TIMEOUT = 3  # seconds


def ml_scam_score(text: str) -> float:
    try:
        response = requests.post(
            HF_API_URL,
            json={"text": text},
            timeout=TIMEOUT
        )
        data = response.json()

        if data.get("label") == "spam":
            return float(data.get("confidence", 0.0))
        return 0.0

    except Exception:
        # Fail safe: ML failure should NOT break system
        return 0.0

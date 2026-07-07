from __future__ import annotations

from typing import Dict, List, Tuple

from .database import fetch_crop_profiles


def normalize(value: float, min_value: float, max_value: float) -> float:
    if max_value == min_value:
        return 1.0
    return max(0.0, min(1.0, (value - min_value) / (max_value - min_value)))


def score_crop(payload: Dict[str, float], profile: Dict[str, object]) -> Tuple[float, str]:
    n = payload["nitrogen"]
    p = payload["phosphorous"]
    k = payload["potassium"]
    temp = payload["temperature"]
    humidity = payload["humidity"]
    ph = payload["ph"]
    rainfall = payload["rainfall"]

    n_score = 1.0 - abs(n - ((float(profile["n_min"]) + float(profile["n_max"])) / 2.0)) / 100.0
    p_score = 1.0 - abs(p - ((float(profile["p_min"]) + float(profile["p_max"])) / 2.0)) / 100.0
    k_score = 1.0 - abs(k - ((float(profile["k_min"]) + float(profile["k_max"])) / 2.0)) / 100.0
    temp_score = 1.0 - abs(temp - ((float(profile["temp_min"]) + float(profile["temp_max"])) / 2.0)) / 50.0
    humidity_score = 1.0 - abs(humidity - ((float(profile["humidity_min"]) + float(profile["humidity_max"])) / 2.0)) / 100.0
    ph_score = 1.0 - abs(ph - ((float(profile["ph_min"]) + float(profile["ph_max"])) / 2.0)) / 10.0
    rainfall_score = 1.0 - abs(rainfall - ((float(profile["rainfall_min"]) + float(profile["rainfall_max"])) / 2.0)) / 200.0

    score = (n_score + p_score + k_score + temp_score + humidity_score + ph_score + rainfall_score) / 7.0
    score = max(0.0, min(1.0, score))

    reason = (
        f"{profile['crop_name']} is well-aligned with the supplied soil and climate values."
        if score >= 0.7
        else f"{profile['crop_name']} shows moderate fit and may need additional irrigation or soil amendments."
    )
    return round(score * 100.0, 2), reason


def recommend_crops(payload: Dict[str, float]) -> List[Dict[str, object]]:
    profiles = fetch_crop_profiles()
    scored = []
    for profile in profiles:
        score, reason = score_crop(payload, profile)
        scored.append(
            {
                "crop_name": profile["crop_name"],
                "score": score,
                "reason": reason,
                "description": profile["description"],
                "productivity": profile["productivity"],
            }
        )
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:5]


def evaluate_crop(payload: Dict[str, float], crop_name: str) -> Dict[str, object]:
    profiles = fetch_crop_profiles()
    profile = next((item for item in profiles if item["crop_name"].lower() == crop_name.lower()), None)
    if not profile:
        raise ValueError(f"Crop '{crop_name}' was not found")
    score, reason = score_crop(payload, profile)
    return {
        "crop_name": profile["crop_name"],
        "score": score,
        "reason": reason,
        "description": profile["description"],
        "productivity": profile["productivity"],
    }

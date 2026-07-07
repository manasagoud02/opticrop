from app.ml import recommend_crops


def test_recommendation_returns_top_five():
    payload = {
        "nitrogen": 90,
        "phosphorous": 45,
        "potassium": 40,
        "temperature": 24,
        "humidity": 77,
        "ph": 6.2,
        "rainfall": 160,
    }
    results = recommend_crops(payload)
    assert len(results) <= 5
    assert all("crop_name" in item for item in results)

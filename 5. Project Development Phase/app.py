import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

# Max parameter values for radar chart scaling
RADAR_MAX = {"N": 140, "P": 145, "K": 205, "temperature": 45, "humidity": 100, "ph": 14, "rainfall": 300}

# Crop styling for generated images
CROP_STYLES = {
    'rice': {'color': '#C8A882', 'accent': '#8B7500', 'bg': '#F0E68C'},
    'paddy': {'color': '#C8A882', 'accent': '#8B7500', 'bg': '#F0E68C'},
    'maize': {'color': '#FFD700', 'accent': '#228B22', 'bg': '#FFF8DC'},
    'chickpea': {'color': '#D2691E', 'accent': '#8B4513', 'bg': '#FFE4E1'},
    'kidneybeans': {'color': '#8B0000', 'accent': '#FF6347', 'bg': '#FFF0F5'},
    'pigeonpeas': {'color': '#B8860B', 'accent': '#DAA520', 'bg': '#FFFACD'},
    'mothbeans': {'color': '#CD853F', 'accent': '#8B4513', 'bg': '#F5DEB3'},
    'mungbean': {'color': '#556B2F', 'accent': '#6B8E23', 'bg': '#F0FFF0'},
    'blackgram': {'color': '#1A1A1A', 'accent': '#333333', 'bg': '#F5F5F5'},
    'lentil': {'color': '#A0522D', 'accent': '#8B4513', 'bg': '#FFE4E1'},
    'pomegranate': {'color': '#DC143C', 'accent': '#8B0000', 'bg': '#FFF8DC'},
    'banana': {'color': '#FFD700', 'accent': '#FFA500', 'bg': '#FFFACD'},
    'mango': {'color': '#FF8C00', 'accent': '#FF6347', 'bg': '#FFE4B5'},
    'grapes': {'color': '#800080', 'accent': '#4B0082', 'bg': '#F0E6FF'},
    'watermelon': {'color': '#FF1493', 'accent': '#FF69B4', 'bg': '#F5FFFA'},
    'muskmelon': {'color': '#FF9933', 'accent': '#FF7F50', 'bg': '#F5F5DC'},
    'apple': {'color': '#DC143C', 'accent': '#FF6347', 'bg': '#F0F8FF'},
    'orange': {'color': '#FF8C00', 'accent': '#FFA500', 'bg': '#FFF8DC'},
    'papaya': {'color': '#FFA07A', 'accent': '#FF7F50', 'bg': '#FFF5EE'},
    'coconut': {'color': '#8B4513', 'accent': '#A0522D', 'bg': '#F0FFFF'},
    'cotton': {'color': '#FFFFFF', 'accent': '#D3D3D3', 'bg': '#F5F5F5'},
    'jute': {'color': '#DAA520', 'accent': '#8B7355', 'bg': '#F5F5DC'},
    'coffee': {'color': '#6F4E37', 'accent': '#8B5A3C', 'bg': '#FAF0E6'},
    'wheat': {'color': '#F5DEB3', 'accent': '#8B7500', 'bg': '#FFF8DC'},
    'sugarcane': {'color': '#2E8B57', 'accent': '#006400', 'bg': '#F5FFFA'},
    'potato': {'color': '#DEB887', 'accent': '#8B4513', 'bg': '#F5F5DC'},
    'tomato': {'color': '#FF6347', 'accent': '#CD5C5C', 'bg': '#FFE4E1'},
    'onion': {'color': '#BA55D3', 'accent': '#8A2BE2', 'bg': '#FFF0F5'},
    'tea': {'color': '#2E8B57', 'accent': '#556B2F', 'bg': '#F0FFF0'},
    'millet': {'color': '#DAA520', 'accent': '#B8860B', 'bg': '#FFFACD'},
    'soybean': {'color': '#E0D8B0', 'accent': '#9E9D24', 'bg': '#F9FBE7'},
    'barley': {'color': '#EEDC82', 'accent': '#CD853F', 'bg': '#FFFBF0'},
    'cabbage': {'color': '#98FB98', 'accent': '#2E8B57', 'bg': '#F0FFF0'},
    'spinach': {'color': '#228B22', 'accent': '#006400', 'bg': '#F0FFF0'},
    'lettuce': {'color': '#7CFC00', 'accent': '#556B2F', 'bg': '#F5FFFA'},
    'pea': {'color': '#32CD32', 'accent': '#228B22', 'bg': '#F0FFF0'},
    'broccoli': {'color': '#008000', 'accent': '#006400', 'bg': '#F5FFFA'},
    'carrot': {'color': '#FF8C00', 'accent': '#D2691E', 'bg': '#FFF8DC'},
    'groundnut': {'color': '#D2B48C', 'accent': '#8B4513', 'bg': '#FAF0E6'},
    'lemon': {'color': '#FFD700', 'accent': '#FF8C00', 'bg': '#FFFDF0'},
    'pineapple': {'color': '#FFD700', 'accent': '#556B2F', 'bg': '#FFF8DC'},
    'garlic': {'color': '#F8F8FF', 'accent': '#D3D3D3', 'bg': '#F5F5F5'},
    'ginger': {'color': '#E6D7B8', 'accent': '#8B7355', 'bg': '#FAF0E6'},
    'turmeric': {'color': '#FFC000', 'accent': '#D2691E', 'bg': '#FFFBF0'},
    'chilli': {'color': '#FF0000', 'accent': '#8B0000', 'bg': '#FFF0F5'},
    'mustard': {'color': '#FFDB58', 'accent': '#DAA520', 'bg': '#FFFDF0'},
    'sunflower': {'color': '#FFD700', 'accent': '#FFA500', 'bg': '#FFFDE0'},
    'lentil': {'color': '#D2691E', 'accent': '#8B4513', 'bg': '#FFE4E1'},
    'cucumber': {'color': '#2E8B57', 'accent': '#008000', 'bg': '#F5FFFA'},
    'pumpkin': {'color': '#FF8C00', 'accent': '#FF7F50', 'bg': '#FFF5EE'}
}

# Crop Guide Profiles
CROP_INFO = {
    "paddy": {
        "label": "Paddy",
        "description": "Thrives in warm, water-rich soils and is a staple rice crop for high-yield irrigation systems.",
        "image": "/api/crop-image/paddy"
    },
    "maize": {
        "label": "Maize",
        "description": "Prefers fertile, well-drained soil and is ideal for warm weather with moderate rainfall.",
        "image": "/api/crop-image/maize"
    },
    "sugarcane": {
        "label": "Sugarcane",
        "description": "Grows best in tropical and subtropical climates with ample water and nutrients.",
        "image": "/api/crop-image/sugarcane"
    },
    "banana": {
        "label": "Banana",
        "description": "Banana plants are best in humid, tropical climates with rich organic soil and steady water supply.",
        "image": "/api/crop-image/banana"
    },
    "orange": {
        "label": "Orange",
        "description": "Orange orchards favor warm climates with good drainage and consistent humidity for sweet, juicy fruit.",
        "image": "/api/crop-image/orange"
    },
    "apple": {
        "label": "Apple",
        "description": "Apple trees perform well in temperate climates and need well-drained soil with regular chill hours.",
        "image": "/api/crop-image/apple"
    },
    "potato": {
        "label": "Potato",
        "description": "Potatoes require cool temperatures, loose soil, and even moisture for healthy tuber formation.",
        "image": "/api/crop-image/potato"
    },
    "chickpea": {
        "label": "Chickpea",
        "description": "A drought-tolerant pulse crop that improves soil nitrogen and suits cooler dry seasons.",
        "image": "/api/crop-image/chickpea"
    },
    "coffee": {
        "label": "Coffee",
        "description": "Coffee grows best in shaded, tropical highlands with rich, acidic soil and regular moisture.",
        "image": "/api/crop-image/coffee"
    },
    "cabbage": {
        "label": "Cabbage",
        "description": "Cabbage grows well in cool weather and prefers fertile, moisture-retentive soil.",
        "image": "/api/crop-image/cabbage"
    },
    "pea": {
        "label": "Pea",
        "description": "Peas prefer cool conditions, well-drained soil, and moderate moisture for strong growth.",
        "image": "/api/crop-image/pea"
    },
    "lettuce": {
        "label": "Lettuce",
        "description": "Lettuce thrives in cool climates with regular moisture and rich, loose soil.",
        "image": "/api/crop-image/lettuce"
    },
    "spinach": {
        "label": "Spinach",
        "description": "Spinach grows best in cool weather and benefits from steady moisture and fertile soil.",
        "image": "/api/crop-image/spinach"
    },
    "rice": {
        "label": "Rice",
        "description": "Rice is a water-loving cereal that performs well in flooded or irrigated lowland fields.",
        "image": "/api/crop-image/rice"
    },
    "millet": {
        "label": "Millet",
        "description": "Millet is a hardy, drought-tolerant cereal suited to warm climates and poor soils.",
        "image": "/api/crop-image/millet"
    },
    "soybean": {
        "label": "Soybean",
        "description": "Soybean grows well in warm climates with fertile soil and moderate rainfall.",
        "image": "/api/crop-image/soybean"
    },
    "tea": {
        "label": "Tea",
        "description": "Tea prefers cool, humid highlands with acidic soil and regular rainfall.",
        "image": "/api/crop-image/tea"
    },
    "cotton": {
        "label": "Cotton",
        "description": "Cotton needs warm weather, bright sunlight, and well-drained soil for high yield.",
        "image": "/api/crop-image/cotton"
    },
    "wheat": {
        "label": "Wheat",
        "description": "Wheat grows best in cool climates with moderate rainfall and fertile loam.",
        "image": "/api/crop-image/wheat"
    },
    "tomato": {
        "label": "Tomato",
        "description": "Tomato crops prefer warm weather, full sun, and rich, well-drained soil.",
        "image": "/api/crop-image/tomato"
    },
    "barley": {
        "label": "Barley",
        "description": "Barley is adapted to cool climates and tolerates drier conditions better than many cereals.",
        "image": "/api/crop-image/barley"
    },
    "grapes": {
        "label": "Grapes",
        "description": "Grapes prefer sunny, warm climates with well-drained soil and careful irrigation.",
        "image": "/api/crop-image/grapes"
    },
    "mango": {
        "label": "Mango",
        "description": "Mango trees flourish in tropical climates with warm temperatures and good drainage.",
        "image": "/api/crop-image/mango"
    },
    "coconut": {
        "label": "Coconut",
        "description": "Coconut palms thrive in tropical coastal climates with high humidity, warm temperatures, and well-drained sandy soil.",
        "image": "/api/crop-image/coconut"
    },
    "onion": {
        "label": "Onion",
        "description": "Onions grow best in cool weather with well-drained, fertile soil and moderate moisture.",
        "image": "/api/crop-image/onion"
    },
    "broccoli": {
        "label": "Broccoli",
        "description": "Broccoli thrives in cool climates with fertile, well-drained soil and consistent moisture.",
        "image": "/api/crop-image/broccoli"
    },
    "carrot": {
        "label": "Carrot",
        "description": "Carrots prefer loose, deep, well-drained soil with cool temperatures for good root development.",
        "image": "/api/crop-image/carrot"
    },
    "groundnut": {
        "label": "Groundnut",
        "description": "Groundnut grows well in warm, sandy loam soil with good drainage and moderate rainfall.",
        "image": "/api/crop-image/groundnut"
    },
    "watermelon": {
        "label": "Watermelon",
        "description": "Watermelon thrives in warm, sunny climates with sandy loam soil and moderate irrigation.",
        "image": "/api/crop-image/watermelon"
    },
    "papaya": {
        "label": "Papaya",
        "description": "Papaya grows fast in tropical climates with rich, well-drained soil and warm temperatures.",
        "image": "/api/crop-image/papaya"
    },
    "pomegranate": {
        "label": "Pomegranate",
        "description": "Pomegranate is drought-tolerant and grows well in hot, dry climates with well-drained soil.",
        "image": "/api/crop-image/pomegranate"
    },
    "lemon": {
        "label": "Lemon",
        "description": "Lemon trees prefer warm, sunny climates with well-drained soil and moderate moisture.",
        "image": "/api/crop-image/lemon"
    },
    "pineapple": {
        "label": "Pineapple",
        "description": "Pineapple grows in tropical climates with acidic, well-drained soil and moderate rainfall.",
        "image": "/api/crop-image/pineapple"
    },
    "garlic": {
        "label": "Garlic",
        "description": "Garlic prefers cool weather, well-drained fertile soil, and moderate moisture.",
        "image": "/api/crop-image/garlic"
    },
    "ginger": {
        "label": "Ginger",
        "description": "Ginger thrives in warm, humid climates with rich, well-drained soil and partial shade.",
        "image": "/api/crop-image/ginger"
    },
    "turmeric": {
        "label": "Turmeric",
        "description": "Turmeric grows best in warm, humid conditions with loamy, well-drained soil.",
        "image": "/api/crop-image/turmeric"
    },
    "chilli": {
        "label": "Chilli",
        "description": "Chilli peppers prefer warm weather, well-drained fertile soil, and moderate irrigation.",
        "image": "/api/crop-image/chilli"
    },
    "mustard": {
        "label": "Mustard",
        "description": "Mustard is a cool-season oilseed crop that grows well in well-drained loamy soil.",
        "image": "/api/crop-image/mustard"
    },
    "sunflower": {
        "label": "Sunflower",
        "description": "Sunflower is a warm-season crop that grows well in well-drained soil with full sun exposure.",
        "image": "/api/crop-image/sunflower"
    },
    "lentil": {
        "label": "Lentil",
        "description": "Lentil is a cool-season pulse that fixes nitrogen and grows well in dry, well-drained soil.",
        "image": "/api/crop-image/lentil"
    },
    "cucumber": {
        "label": "Cucumber",
        "description": "Cucumber grows fast in warm weather with fertile, well-drained soil and consistent moisture.",
        "image": "/api/crop-image/cucumber"
    },
    "pumpkin": {
        "label": "Pumpkin",
        "description": "Pumpkin thrives in warm weather with rich, well-drained soil and plenty of space to spread.",
        "image": "/api/crop-image/pumpkin"
    }
}

CROP_IDEAL = {
    "paddy":    {"N": 80,  "P": 40,  "K": 40,  "temperature": 25, "humidity": 80, "ph": 6.0, "rainfall": 175},
    "maize":    {"N": 80,  "P": 40,  "K": 20,  "temperature": 22, "humidity": 65, "ph": 6.4, "rainfall": 120},
    "sugarcane":{"N": 120, "P": 40,  "K": 50,  "temperature": 25, "humidity": 80, "ph": 6.8, "rainfall": 175},
    "banana":   {"N": 100, "P": 75,  "K": 50,  "temperature": 28, "humidity": 80, "ph": 6.0, "rainfall": 190},
    "orange":   {"N": 20,  "P": 10,  "K": 10,  "temperature": 23, "humidity": 92, "ph": 7.0, "rainfall": 125},
    "apple":    {"N": 20,  "P": 10,  "K": 10,  "temperature": 21, "humidity": 92, "ph": 6.3, "rainfall": 97},
    "potato":   {"N": 120, "P": 40,  "K": 20,  "temperature": 17, "humidity": 80, "ph": 5.5, "rainfall": 92},
    "chickpea": {"N": 40,  "P": 67,  "K": 79,  "temperature": 17, "humidity": 16, "ph": 7.3, "rainfall": 47},
    "coffee":   {"N": 100, "P": 28,  "K": 29,  "temperature": 25, "humidity": 58, "ph": 6.8, "rainfall": 150},
    "cabbage":  {"N": 120, "P": 60,  "K": 50,  "temperature": 15, "humidity": 70, "ph": 6.5, "rainfall": 80},
    "pea":      {"N": 40,  "P": 40,  "K": 40,  "temperature": 15, "humidity": 70, "ph": 6.8, "rainfall": 65},
    "lettuce":  {"N": 60,  "P": 30,  "K": 30,  "temperature": 15, "humidity": 70, "ph": 6.5, "rainfall": 85},
    "spinach":  {"N": 80,  "P": 40,  "K": 40,  "temperature": 15, "humidity": 70, "ph": 6.5, "rainfall": 65},
    "rice":     {"N": 80,  "P": 40,  "K": 40,  "temperature": 27, "humidity": 82, "ph": 6.2, "rainfall": 200},
    "millet":   {"N": 20,  "P": 25,  "K": 25,  "temperature": 30, "humidity": 65, "ph": 6.2, "rainfall": 60},
    "soybean":  {"N": 20,  "P": 45,  "K": 45,  "temperature": 25, "humidity": 65, "ph": 6.5, "rainfall": 80},
    "tea":      {"N": 40,  "P": 25,  "K": 25,  "temperature": 20, "humidity": 80, "ph": 5.2, "rainfall": 200},
    "cotton":   {"N": 120, "P": 40,  "K": 20,  "temperature": 30, "humidity": 65, "ph": 6.4, "rainfall": 75},
    "wheat":    {"N": 100, "P": 40,  "K": 40,  "temperature": 17, "humidity": 65, "ph": 6.8, "rainfall": 70},
    "tomato":   {"N": 80,  "P": 40,  "K": 40,  "temperature": 23, "humidity": 70, "ph": 6.5, "rainfall": 100},
    "barley":   {"N": 60,  "P": 55,  "K": 55,  "temperature": 15, "humidity": 65, "ph": 6.8, "rainfall": 60},
    "grapes":   {"N": 20,  "P": 125, "K": 200, "temperature": 22, "humidity": 80, "ph": 6.5, "rainfall": 80},
    "mango":    {"N": 20,  "P": 27,  "K": 30,  "temperature": 27, "humidity": 50, "ph": 5.7, "rainfall": 162},
    "coconut":  {"N": 22,  "P": 16,  "K": 45,  "temperature": 27, "humidity": 94, "ph": 6.0, "rainfall": 175},
    "onion":    {"N": 50,  "P": 30,  "K": 30,  "temperature": 25, "humidity": 65, "ph": 6.5, "rainfall": 100},
    "broccoli": {"N": 80,  "P": 40,  "K": 40,  "temperature": 18, "humidity": 70, "ph": 6.5, "rainfall": 100},
    "carrot":   {"N": 60,  "P": 40,  "K": 40,  "temperature": 20, "humidity": 65, "ph": 6.5, "rainfall": 100},
    "groundnut":{"N": 25,  "P": 50,  "K": 50,  "temperature": 28, "humidity": 65, "ph": 6.0, "rainfall": 100},
    "watermelon":{"N": 100, "P": 50,  "K": 60,  "temperature": 30, "humidity": 70, "ph": 6.5, "rainfall": 60},
    "papaya":   {"N": 100, "P": 50,  "K": 60,  "temperature": 30, "humidity": 70, "ph": 6.5, "rainfall": 125},
    "pomegranate":{"N": 30, "P": 30, "K": 30,  "temperature": 30, "humidity": 60, "ph": 6.5, "rainfall": 75},
    "lemon":    {"N": 30,  "P": 15,  "K": 15,  "temperature": 25, "humidity": 70, "ph": 6.0, "rainfall": 100},
    "pineapple":{"N": 100, "P": 15,  "K": 120, "temperature": 25, "humidity": 80, "ph": 5.2, "rainfall": 125},
    "garlic":   {"N": 100, "P": 50,  "K": 50,  "temperature": 18, "humidity": 65, "ph": 6.5, "rainfall": 75},
    "ginger":   {"N": 100, "P": 50,  "K": 70,  "temperature": 25, "humidity": 80, "ph": 6.0, "rainfall": 175},
    "turmeric": {"N": 100, "P": 50,  "K": 70,  "temperature": 25, "humidity": 80, "ph": 6.2, "rainfall": 175},
    "chilli":   {"N": 100, "P": 50,  "K": 70,  "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 90},
    "mustard":  {"N": 80,  "P": 40,  "K": 40,  "temperature": 17, "humidity": 65, "ph": 6.8, "rainfall": 60},
    "sunflower":{"N": 80,  "P": 50,  "K": 50,  "temperature": 25, "humidity": 65, "ph": 6.8, "rainfall": 75},
    "lentil":   {"N": 30,  "P": 50,  "K": 30,  "temperature": 20, "humidity": 65, "ph": 7.0, "rainfall": 37},
    "cucumber": {"N": 100, "P": 50,  "K": 60,  "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 80},
    "pumpkin":  {"N": 100, "P": 50,  "K": 60,  "temperature": 23, "humidity": 70, "ph": 6.8, "rainfall": 80},
}

def load_ml_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        # Fallback to train standard Random Forest model on dataset
        import subprocess
        print("Model or scaler not found. Running training script...")
        subprocess.run(["python", "compare_models.py"], cwd=BASE_DIR, check=True)
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

MODEL, SCALER = load_ml_model()

def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    df_features = pd.DataFrame([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]], columns=FEATURE_COLUMNS)
    scaled_features = SCALER.transform(df_features)
    prediction = MODEL.predict(scaled_features)[0]
    return prediction

def get_crop_info(crop):
    return CROP_INFO.get(crop.lower(), {
        'label': crop.title(),
        'description': 'A recommended crop based on your soil and weather conditions.',
        'image': '/api/crop-image/default'
    })

def calculate_match_score(radar_user, radar_ideal):
    diffs = [abs(radar_user[i] - radar_ideal[i]) for i in range(len(radar_user))]
    avg_diff = sum(diffs) / len(diffs)
    
    if avg_diff <= 12:
        return "excellent", "Your field conditions are an excellent match for this crop. Go ahead and plant with confidence!", "success", "bi-check-circle-fill"
    elif avg_diff <= 25:
        return "good", "Your field is a good match. Minor adjustments may improve yield.", "primary", "bi-check-circle"
    else:
        return "best_available", "This is the best crop for your conditions among available options.", "info", "bi-info-circle-fill"

def get_parameter_advice(radar_user, radar_ideal, radar_labels):
    param_advice = []
    for i, k in enumerate(radar_labels):
        diff = radar_user[i] - radar_ideal[i]
        if abs(diff) > 15:
            if diff < 0:
                param_advice.append({"param": k, "status": "low", "msg": f"{k} is too low — consider increasing it."})
            else:
                param_advice.append({"param": k, "status": "high", "msg": f"{k} is too high — consider reducing it."})
    return param_advice

# --- PIL Crop Image Generator Helpers ---
def draw_rice_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(50, width, 80):
        for y_offset in range(-5, 10, 5):
            stalk_x = x + y_offset
            draw.line([(stalk_x, soil_top), (stalk_x - 15, soil_top - 80)], fill=(139, 120, 93), width=2)
            draw.line([(stalk_x, soil_top), (stalk_x + 15, soil_top - 75)], fill=(139, 120, 93), width=2)
            draw.ellipse([stalk_x - 8, soil_top - 85, stalk_x + 8, soil_top - 70], 
                        fill=(184, 134, 11), outline=(139, 105, 10), width=1)

def draw_maize_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(80, width, 120):
        draw.line([(x, soil_top), (x, soil_top - 150)], fill=(34, 139, 34), width=4)
        for i in range(5):
            leaf_y = soil_top - (30 + i * 25)
            draw.polygon([(x, leaf_y), (x - 25, leaf_y - 15), (x - 15, leaf_y - 20)], fill=(76, 175, 80))
            draw.polygon([(x, leaf_y), (x + 25, leaf_y - 15), (x + 15, leaf_y - 20)], fill=(56, 142, 60))
        draw.ellipse([x - 12, soil_top - 160, x + 12, soil_top - 120], fill=(184, 134, 11), outline=(139, 105, 10), width=1)

def draw_legume_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(60, width, 100):
        draw.line([(x, soil_top), (x - 10, soil_top - 60)], fill=(34, 139, 34), width=2)
        draw.line([(x, soil_top), (x + 10, soil_top - 65)], fill=(34, 139, 34), width=2)
        draw.ellipse([x - 15, soil_top - 75, x, soil_top - 55], fill=(85, 180, 85))
        draw.ellipse([x, soil_top - 70, x + 15, soil_top - 50], fill=(76, 175, 80))
        draw.ellipse([x - 8, soil_top - 90, x + 8, soil_top - 75], fill=(107, 142, 35))

def draw_fruit_trees(draw, width, height, styles, crop_name):
    soil_top = int(height * 0.65)
    tree_x = width // 2
    draw.rectangle([tree_x - 15, soil_top - 180, tree_x + 15, soil_top], fill=(139, 69, 19), outline=(101, 50, 15))
    canopy_radius = 80
    canopy_color = (34, 139, 34) if crop_name != 'coconut' else (107, 142, 35)
    draw.ellipse([tree_x - canopy_radius, soil_top - 200 - canopy_radius, 
                  tree_x + canopy_radius, soil_top - 200 + canopy_radius], 
                fill=canopy_color, outline=(25, 100, 25), width=2)
    fruit_color = styles.get('color', '#FFD700')
    fruit_hex = fruit_color.lstrip('#')
    fruit_rgb = tuple(int(fruit_hex[i:i+2], 16) for i in (0, 2, 4))
    for i in range(5):
        fruit_x = tree_x - 60 + i * 30
        fruit_y = soil_top - 200 + (i % 2) * 30
        draw.ellipse([fruit_x - 12, fruit_y - 12, fruit_x + 12, fruit_y + 12], fill=fruit_rgb, outline=(200, 140, 50), width=1)

def draw_trailing_plants(draw, width, height, styles, crop_name):
    soil_top = int(height * 0.65)
    for i in range(3):
        start_x = 100 + i * 180
        for j in range(4):
            vine_y = soil_top - 50 - j * 40
            draw.line([(start_x, soil_top), (start_x + 30, vine_y)], fill=(34, 139, 34), width=3)
            fruit_color = styles.get('color', '#FF69B4')
            fruit_hex = fruit_color.lstrip('#')
            fruit_rgb = tuple(int(fruit_hex[k:k+2], 16) for k in (0, 2, 4))
            for k in range(3):
                draw.ellipse([start_x + 20 + k*8, vine_y - 20 + k*6, start_x + 28 + k*8, vine_y - 12 + k*6], fill=fruit_rgb)

def draw_citrus_trees(draw, width, height, styles, crop_name):
    soil_top = int(height * 0.65)
    for tree_x in [150, 450]:
        draw.rectangle([tree_x - 10, soil_top - 120, tree_x + 10, soil_top], fill=(139, 69, 19))
        draw.ellipse([tree_x - 60, soil_top - 180, tree_x + 60, soil_top - 60], fill=(34, 139, 34), outline=(25, 100, 25), width=2)
        fruit_color = styles.get('color', '#FF8C00')
        fruit_hex = fruit_color.lstrip('#')
        fruit_rgb = tuple(int(fruit_hex[i:i+2], 16) for i in (0, 2, 4))
        for i in range(6):
            fruit_x = tree_x - 40 + (i % 3) * 40
            fruit_y = soil_top - 100 - (i // 3) * 40
            draw.ellipse([fruit_x - 10, fruit_y - 10, fruit_x + 10, fruit_y + 10], fill=fruit_rgb, outline=(200, 120, 40))

def draw_cotton_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(100, width, 150):
        draw.line([(x, soil_top), (x, soil_top - 100)], fill=(34, 139, 34), width=3)
        for i in range(4):
            leaf_y = soil_top - 25 - i * 20
            draw.polygon([(x, leaf_y), (x - 20, leaf_y - 10), (x - 15, leaf_y + 10)], fill=(85, 180, 85))
        for i in range(3):
            boll_x = x - 30 + i * 30
            boll_y = soil_top - 80 + (i % 2) * 20
            draw.ellipse([boll_x - 15, boll_y - 15, boll_x + 15, boll_y + 15], fill=(240, 240, 240), outline=(200, 200, 200), width=1)

def draw_jute_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(80, width, 140):
        draw.line([(x, soil_top), (x - 5, soil_top - 130)], fill=(139, 105, 20), width=3)
        draw.line([(x, soil_top), (x + 5, soil_top - 125)], fill=(139, 105, 20), width=3)
        for i in range(5):
            leaf_y = soil_top - 40 - i * 15
            draw.polygon([(x, leaf_y), (x - 15, leaf_y - 8), (x + 12, leaf_y - 5)], fill=(107, 142, 35))
        draw.ellipse([x - 8, soil_top - 135, x + 8, soil_top - 120], fill=(210, 180, 140))

def draw_coffee_plants(draw, width, height, styles):
    soil_top = int(height * 0.6)
    for x in range(100, width, 160):
        draw.ellipse([x - 35, soil_top - 100, x + 35, soil_top - 30], fill=(34, 139, 34), outline=(25, 100, 25), width=2)
        for i in range(5):
            berry_x = x - 25 + i * 15
            berry_y = soil_top - 90 + (i % 2) * 15
            draw.ellipse([berry_x - 6, berry_y - 6, berry_x + 6, berry_y + 6], fill=(139, 35, 35))

def draw_generic_crop(draw, width, height, styles):
    soil_top = int(height * 0.6)
    crop_color = styles.get('color', '#32CD32')
    crop_hex = crop_color.lstrip('#')
    crop_rgb = tuple(int(crop_hex[i:i+2], 16) for i in (0, 2, 4))
    for x in range(60, width, 100):
        draw.line([(x, soil_top), (x - 10, soil_top - 80)], fill=(34, 139, 34), width=2)
        draw.line([(x, soil_top), (x + 10, soil_top - 75)], fill=(34, 139, 34), width=2)
        draw.ellipse([x - 18, soil_top - 85, x + 18, soil_top - 60], fill=crop_rgb, outline=(25, 100, 25), width=1)

def generate_crop_image(crop_name):
    width, height = 600, 400
    styles = CROP_STYLES.get(crop_name, CROP_STYLES.get('rice'))
    
    img = Image.new('RGB', (width, height), (135, 206, 235))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Sky gradient
    for y in range(height):
        ratio = y / height
        r = int(135 * (1 - ratio) + 101 * ratio)
        g = int(206 * (1 - ratio) + 155 * ratio)
        b = int(235 * (1 - ratio) + 50 * ratio)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b, 255))
    
    # Ground/soil gradient
    soil_height = height // 2.5
    for y in range(height - int(soil_height), height):
        ratio = (y - (height - int(soil_height))) / int(soil_height)
        r = int(139 * (1 - ratio) + 101 * ratio)
        g = int(90 * (1 - ratio) + 67 * ratio)
        b = int(43 * (1 - ratio) + 33 * ratio)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b, 255))
    
    # Draw elements
    if crop_name in ['rice', 'paddy']:
        draw_rice_plants(draw, width, height, styles)
    elif crop_name == 'maize':
        draw_maize_plants(draw, width, height, styles)
    elif crop_name in ['chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'soybean', 'pea']:
        draw_legume_plants(draw, width, height, styles)
    elif crop_name in ['banana', 'mango', 'papaya', 'coconut']:
        draw_fruit_trees(draw, width, height, styles, crop_name)
    elif crop_name in ['grapes', 'watermelon', 'muskmelon', 'cucumber', 'pumpkin']:
        draw_trailing_plants(draw, width, height, styles, crop_name)
    elif crop_name in ['pomegranate', 'apple', 'orange', 'lemon']:
        draw_citrus_trees(draw, width, height, styles, crop_name)
    elif crop_name == 'cotton':
        draw_cotton_plants(draw, width, height, styles)
    elif crop_name == 'jute':
        draw_jute_plants(draw, width, height, styles)
    elif crop_name in ['coffee', 'tea']:
        draw_coffee_plants(draw, width, height, styles)
    else:
        draw_generic_crop(draw, width, height, styles)
    
    # Header Banner
    banner_height = 60
    draw.rectangle([0, 0, width, banner_height], fill=(0, 0, 0, 180))
    
    try:
        title_font = ImageFont.load_default()
    except:
        title_font = None
    
    crop_label = CROP_INFO.get(crop_name, {}).get('label', crop_name.title())
    
    # Draw Text
    draw.text((20, 15), f"OPTI-CROP Recommendations: {crop_label}", fill='white', font=title_font)
    
    return img.convert('RGB')

@app.route('/api/crop-image/<crop_name>')
def crop_image(crop_name):
    try:
        img = generate_crop_image(crop_name.lower())
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or request.form
    try:
        user_input = {
            'N': float(data.get('nitrogen', data.get('N', 0))),
            'P': float(data.get('phosphorus', data.get('P', 0))),
            'K': float(data.get('potassium', data.get('K', 0))),
            'temperature': float(data.get('temperature', 0)),
            'humidity': float(data.get('humidity', 0)),
            'ph': float(data.get('ph', 0)),
            'rainfall': float(data.get('rainfall', 0))
        }
    except (ValueError, TypeError):
        return jsonify({'error': 'Please enter valid numeric values for all parameters.'}), 400

    if any(val < 0 for val in user_input.values()):
        return jsonify({'error': 'Parameters cannot be negative.'}), 400

    try:
        df_features = pd.DataFrame([[user_input[col] for col in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]], columns=FEATURE_COLUMNS)
        scaled_features = SCALER.transform(df_features)
        
        prediction = MODEL.predict(scaled_features)[0]
        proba = MODEL.predict_proba(scaled_features)[0]
        
        crop_name = prediction.lower()
        crop_info = get_crop_info(crop_name)
        ideal = CROP_IDEAL.get(crop_name, {})
        
        # Scale comparison arrays for radar chart
        radar_labels = FEATURE_COLUMNS
        radar_user = [round(user_input[k] / RADAR_MAX[k] * 100, 1) for k in radar_labels]
        radar_ideal = [round(ideal.get(k, 0) / RADAR_MAX[k] * 100, 1) for k in radar_labels]
        
        # Calculate Match Scores & Advice
        match_status, match_message, match_color, match_icon = calculate_match_score(radar_user, radar_ideal)
        param_advice = get_parameter_advice(radar_user, radar_ideal, radar_labels)
        
        # Get top 3 alternatives
        top_indices = np.argsort(proba)[::-1][:3]
        top3 = []
        for idx in top_indices:
            alternative_crop = MODEL.classes_[idx]
            alt_info = get_crop_info(alternative_crop)
            top3.append({
                'crop': alternative_crop,
                'label': alt_info['label'],
                'confidence': round(proba[idx] * 100, 1)
            })
            
        return jsonify({
            'crop': prediction,
            'label': crop_info['label'],
            'description': crop_info['description'],
            'image': crop_info['image'],
            'top3': top3,
            'radar_labels': radar_labels,
            'radar_user': radar_user,
            'radar_ideal': radar_ideal,
            'match_status': match_status,
            'match_message': match_message,
            'match_color': match_color,
            'match_icon': match_icon,
            'param_advice': param_advice,
            'inputs': user_input
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

import os
import pickle
from flask import Flask, render_template, request, session, send_from_directory
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "opti-crop-default-key")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "crop_recommendation_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

CROP_GUIDE = {
    "paddy": {
        "summary": "Paddy thrives in warm, water-rich soils and is a staple rice crop for high-yield irrigation systems.",
        "ph": "5.5 - 6.5",
        "temperature": "20 - 30°C",
        "rainfall": "150 - 200 mm",
        "touchpoints": ["Use well-distributed irrigation", "Maintain balanced NPK levels", "Monitor water depth closely"],
        "image": "img/paddy.jpg"
    },
    "maize": {
        "summary": "Maize prefers fertile, well-drained soil and is ideal for warm weather with moderate rainfall.",
        "ph": "5.8 - 7.0",
        "temperature": "18 - 27°C",
        "rainfall": "90 - 150 mm",
        "touchpoints": ["Apply nitrogen-rich fertilizer early", "Ensure consistent moisture", "Use crop rotation to preserve soil health"],
        "image": "img/maize.jpg"
    },
    "sugarcane": {
        "summary": "Sugarcane grows best in tropical and subtropical climates with ample water and nutrients.",
        "ph": "6.0 - 7.5",
        "temperature": "20 - 30°C",
        "rainfall": "150 - 200 mm",
        "touchpoints": ["Keep soil moisture high", "Use potassium-rich fertilizer", "Maintain clean crop rows"],
        "image": "img/sugarcane.jpg"
    },
    "banana": {
        "summary": "Banana plants are best in humid, tropical climates with rich organic soil and steady water supply.",
        "ph": "5.5 - 6.5",
        "temperature": "26 - 30°C",
        "rainfall": "160 - 220 mm",
        "touchpoints": ["Ensure deep, regular watering", "Mulch to conserve moisture", "Use balanced fertilizer with magnesium"],
        "image": "img/banana.jpg"
    },
    "orange": {
        "summary": "Orange orchards favor warm climates with good drainage and consistent humidity for sweet, juicy fruit.",
        "ph": "5.5 - 6.5",
        "temperature": "18 - 29°C",
        "rainfall": "100 - 150 mm",
        "touchpoints": ["Protect from frost", "Ensure full sun exposure", "Feed with micronutrient supplements"],
        "image": "img/orange.jpg"
    },
    "apple": {
        "summary": "Apple trees perform well in temperate climates and need well-drained soil with regular chill hours.",
        "ph": "5.8 - 6.8",
        "temperature": "18 - 24°C",
        "rainfall": "75 - 120 mm",
        "touchpoints": ["Prune annually", "Maintain consistent irrigation", "Monitor pests and diseases"],
        "image": "img/apple.jpg"
    },
    "potato": {
        "summary": "Potatoes require cool temperatures, loose soil, and even moisture for healthy tuber formation.",
        "ph": "5.0 - 6.0",
        "temperature": "15 - 20°C",
        "rainfall": "75 - 110 mm",
        "touchpoints": ["Avoid waterlogging", "Hill soil around stems", "Use phosphorus-rich fertilizer"],
        "image": "img/potato.jpg"
    },
    "chickpea": {
        "summary": "Chickpea is a drought-tolerant pulse crop that improves soil nitrogen and suits cooler dry seasons.",
        "ph": "6.0 - 7.0",
        "temperature": "10 - 25°C",
        "rainfall": "35 - 60 mm",
        "touchpoints": ["Plant in well-drained soil", "Use crop rotation with cereals", "Monitor for pests in dry weather"],
        "image": "img/chickpea.jpg"
    },
    "coffee": {
        "summary": "Coffee grows best in shaded, tropical highlands with rich, acidic soil and regular moisture.",
        "ph": "5.0 - 6.5",
        "temperature": "18 - 24°C",
        "rainfall": "120 - 180 mm",
        "touchpoints": ["Provide partial shade", "Mulch for moisture management", "Apply organic matter frequently"],
        "image": "img/coffee.jpg"
    },
    "cabbage": {
        "summary": "Cabbage grows well in cool weather and prefers fertile, moisture-retentive soil.",
        "ph": "6.0 - 7.0",
        "temperature": "10 - 20°C",
        "rainfall": "60 - 100 mm",
        "touchpoints": ["Keep soil evenly moist", "Use balanced nitrogen feeding", "Protect from heat stress"],
        "image": "img/cabbage.jpg"
    },
    "pea": {
        "summary": "Peas prefer cool conditions, well-drained soil, and moderate moisture for strong growth.",
        "ph": "6.0 - 7.5",
        "temperature": "10 - 20°C",
        "rainfall": "50 - 80 mm",
        "touchpoints": ["Avoid waterlogging", "Provide support for climbing varieties", "Rotate with cereals"],
        "image": "img/pea.jpg"
    },
    "lettuce": {
        "summary": "Lettuce thrives in cool climates with regular moisture and rich, loose soil.",
        "ph": "6.0 - 7.0",
        "temperature": "10 - 20°C",
        "rainfall": "70 - 100 mm",
        "touchpoints": ["Maintain consistent watering", "Protect from bolting in heat", "Use shade during hot spells"],
        "image": "img/lettuce.jpg"
    },
    "spinach": {
        "summary": "Spinach grows best in cool weather and benefits from steady moisture and fertile soil.",
        "ph": "6.0 - 7.0",
        "temperature": "10 - 20°C",
        "rainfall": "50 - 80 mm",
        "touchpoints": ["Harvest young leaves regularly", "Keep soil evenly moist", "Avoid high heat exposure"],
        "image": "img/spinach.jpg"
    },
    "rice": {
        "summary": "Rice is a water-loving cereal that performs well in flooded or irrigated lowland fields.",
        "ph": "5.5 - 7.0",
        "temperature": "20 - 35°C",
        "rainfall": "150 - 250 mm",
        "touchpoints": ["Maintain standing water when needed", "Use nutrient-rich flooded soils", "Manage weeds early"],
        "image": "img/rice.jpeg"
    },
    "millet": {
        "summary": "Millet is a hardy, drought-tolerant cereal suited to warm climates and poor soils.",
        "ph": "5.5 - 7.0",
        "temperature": "25 - 35°C",
        "rainfall": "40 - 80 mm",
        "touchpoints": ["Use low-input management", "Plant in well-drained soil", "Avoid overwatering"],
        "image": "img/millet.jpg"
    },
    "soybean": {
        "summary": "Soybean grows well in warm climates with fertile soil and moderate rainfall.",
        "ph": "6.0 - 7.0",
        "temperature": "20 - 30°C",
        "rainfall": "60 - 100 mm",
        "touchpoints": ["Ensure good nodulation", "Use crop rotation with cereals", "Monitor for pests"],
        "image": "img/soybean.jpg"
    },
    "tea": {
        "summary": "Tea prefers cool, humid highlands with acidic soil and regular rainfall.",
        "ph": "4.5 - 6.0",
        "temperature": "15 - 25°C",
        "rainfall": "150 - 250 mm",
        "touchpoints": ["Maintain shade and humidity", "Use acidic fertilizer carefully", "Prune regularly"],
        "image": "img/tea.webp"
    },
    "cotton": {
        "summary": "Cotton needs warm weather, bright sunlight, and well-drained soil for high yield.",
        "ph": "5.8 - 7.0",
        "temperature": "25 - 35°C",
        "rainfall": "50 - 100 mm",
        "touchpoints": ["Provide full sun", "Use timely irrigation", "Monitor pests and boll health"],
        "image": "img/cotton.jpg"
    },
    "wheat": {
        "summary": "Wheat grows best in cool climates with moderate rainfall and fertile loam.",
        "ph": "6.0 - 7.5",
        "temperature": "10 - 25°C",
        "rainfall": "50 - 90 mm",
        "touchpoints": ["Use proper seeding depth", "Apply nitrogen at key stages", "Protect against lodging"],
        "image": "img/wheat.jpg"
    },
    "tomato": {
        "summary": "Tomato crops prefer warm weather, full sun, and rich, well-drained soil.",
        "ph": "6.0 - 7.0",
        "temperature": "20 - 27°C",
        "rainfall": "80 - 120 mm",
        "touchpoints": ["Support the plants", "Mulch to conserve moisture", "Watch for fungal disease"],
        "image": "img/tomato.jpg"
    },
    "barley": {
        "summary": "Barley is adapted to cool climates and tolerates drier conditions better than many cereals.",
        "ph": "6.0 - 7.5",
        "temperature": "10 - 20°C",
        "rainfall": "40 - 80 mm",
        "touchpoints": ["Use well-drained fields", "Apply balanced nutrients", "Avoid excess moisture"],
        "image": "img/barley.jpg"
    },
    "grapes": {
        "summary": "Grapes prefer sunny, warm climates with well-drained soil and careful irrigation.",
        "ph": "6.0 - 7.0",
        "temperature": "15 - 30°C",
        "rainfall": "60 - 100 mm",
        "touchpoints": ["Provide full sun", "Prune annually", "Use trellising and canopy management"],
        "image": "img/grapes.jpg"
    },
    "mango": {
        "summary": "Mango trees flourish in tropical climates with warm temperatures and good drainage.",
        "ph": "5.5 - 7.5",
        "temperature": "24 - 30°C",
        "rainfall": "75 - 250 mm",
        "touchpoints": ["Ensure good drainage", "Use organic matter in the root zone", "Protect young trees from cold"],
        "image": "img/mango.jpg"
    },
    "coconut": {
        "summary": "Coconut palms thrive in tropical coastal climates with high humidity, warm temperatures, and well-drained sandy soil.",
        "ph": "5.5 - 8.0",
        "temperature": "20 - 32°C",
        "rainfall": "150 - 250 mm",
        "touchpoints": ["Ensure good drainage to avoid root rot", "Apply potassium-rich fertilizer regularly", "Maintain high humidity around young palms"],
        "image": "img/coconut.jpg"
    },
    "onion": {
        "summary": "Onions grow best in cool weather with well-drained, fertile soil and moderate moisture.",
        "ph": "6.0 - 7.0",
        "temperature": "13 - 24°C",
        "rainfall": "70 - 100 mm",
        "touchpoints": ["Avoid waterlogging", "Use sulfur-rich fertilizer", "Harvest when tops fall over"],
        "image": "img/default_hero.jpg"
    },
    "broccoli": {
        "summary": "Broccoli thrives in cool climates with fertile, well-drained soil and consistent moisture.",
        "ph": "6.0 - 7.0",
        "temperature": "15 - 20°C",
        "rainfall": "80 - 120 mm",
        "touchpoints": ["Plant in full sun", "Keep soil consistently moist", "Harvest before flowers open"],
        "image": "img/default_hero.jpg"
    },
    "carrot": {
        "summary": "Carrots prefer loose, deep, well-drained soil with cool temperatures for good root development.",
        "ph": "6.0 - 6.8",
        "temperature": "15 - 20°C",
        "rainfall": "75 - 100 mm",
        "touchpoints": ["Loosen soil deeply before planting", "Thin seedlings for proper spacing", "Avoid excess nitrogen"],
        "image": "img/default_hero.jpg"
    },
    "groundnut": {
        "summary": "Groundnut grows well in warm, sandy loam soil with good drainage and moderate rainfall.",
        "ph": "5.5 - 7.0",
        "temperature": "25 - 30°C",
        "rainfall": "60 - 150 mm",
        "touchpoints": ["Ensure well-drained sandy soil", "Apply calcium at pegging stage", "Avoid waterlogging during pod fill"],
        "image": "img/default_hero.jpg"
    },
    "watermelon": {
        "summary": "Watermelon thrives in warm, sunny climates with sandy loam soil and moderate irrigation.",
        "ph": "6.0 - 7.0",
        "temperature": "25 - 35°C",
        "rainfall": "40 - 80 mm",
        "touchpoints": ["Provide full sun", "Use drip irrigation", "Avoid overhead watering"],
        "image": "img/default_hero.jpg"
    },
    "papaya": {
        "summary": "Papaya grows fast in tropical climates with rich, well-drained soil and warm temperatures.",
        "ph": "6.0 - 7.0",
        "temperature": "25 - 35°C",
        "rainfall": "100 - 150 mm",
        "touchpoints": ["Avoid waterlogging", "Provide wind protection", "Fertilize regularly"],
        "image": "img/default_hero.jpg"
    },
    "pomegranate": {
        "summary": "Pomegranate is drought-tolerant and grows well in hot, dry climates with well-drained soil.",
        "ph": "5.5 - 7.5",
        "temperature": "25 - 35°C",
        "rainfall": "50 - 100 mm",
        "touchpoints": ["Tolerates drought once established", "Prune for open canopy", "Avoid excess moisture"],
        "image": "img/default_hero.jpg"
    },
    "lemon": {
        "summary": "Lemon trees prefer warm, sunny climates with well-drained soil and moderate moisture.",
        "ph": "5.5 - 6.5",
        "temperature": "20 - 30°C",
        "rainfall": "75 - 125 mm",
        "touchpoints": ["Protect from frost", "Use citrus-specific fertilizer", "Ensure good drainage"],
        "image": "img/default_hero.jpg"
    },
    "pineapple": {
        "summary": "Pineapple grows in tropical climates with acidic, well-drained soil and moderate rainfall.",
        "ph": "4.5 - 6.0",
        "temperature": "20 - 30°C",
        "rainfall": "100 - 150 mm",
        "touchpoints": ["Use acidic fertilizer", "Avoid waterlogging", "Mulch to retain moisture"],
        "image": "img/default_hero.jpg"
    },
    "garlic": {
        "summary": "Garlic prefers cool weather, well-drained fertile soil, and moderate moisture.",
        "ph": "6.0 - 7.0",
        "temperature": "12 - 24°C",
        "rainfall": "50 - 100 mm",
        "touchpoints": ["Plant cloves pointed side up", "Avoid excess nitrogen", "Reduce water before harvest"],
        "image": "img/default_hero.jpg"
    },
    "ginger": {
        "summary": "Ginger thrives in warm, humid climates with rich, well-drained soil and partial shade.",
        "ph": "5.5 - 6.5",
        "temperature": "20 - 30°C",
        "rainfall": "150 - 200 mm",
        "touchpoints": ["Provide partial shade", "Keep soil moist but not waterlogged", "Mulch heavily"],
        "image": "img/default_hero.jpg"
    },
    "turmeric": {
        "summary": "Turmeric grows best in warm, humid conditions with loamy, well-drained soil.",
        "ph": "5.5 - 7.0",
        "temperature": "20 - 30°C",
        "rainfall": "150 - 200 mm",
        "touchpoints": ["Plant rhizomes in raised beds", "Maintain high humidity", "Harvest after leaves dry"],
        "image": "img/default_hero.jpg"
    },
    "chilli": {
        "summary": "Chilli peppers prefer warm weather, well-drained fertile soil, and moderate irrigation.",
        "ph": "6.0 - 7.0",
        "temperature": "20 - 30°C",
        "rainfall": "60 - 120 mm",
        "touchpoints": ["Avoid waterlogging", "Use potassium-rich fertilizer at fruiting", "Stake tall plants"],
        "image": "img/default_hero.jpg"
    },
    "mustard": {
        "summary": "Mustard is a cool-season oilseed crop that grows well in well-drained loamy soil.",
        "ph": "6.0 - 7.5",
        "temperature": "10 - 25°C",
        "rainfall": "40 - 80 mm",
        "touchpoints": ["Sow in cool season", "Apply sulfur fertilizer", "Harvest before pods shatter"],
        "image": "img/default_hero.jpg"
    },
    "sunflower": {
        "summary": "Sunflower is a warm-season crop that grows well in well-drained soil with full sun exposure.",
        "ph": "6.0 - 7.5",
        "temperature": "20 - 30°C",
        "rainfall": "50 - 100 mm",
        "touchpoints": ["Provide full sun", "Avoid excess nitrogen", "Harvest when back of head turns yellow"],
        "image": "img/default_hero.jpg"
    },
    "lentil": {
        "summary": "Lentil is a cool-season pulse that fixes nitrogen and grows well in dry, well-drained soil.",
        "ph": "6.0 - 8.0",
        "temperature": "15 - 25°C",
        "rainfall": "25 - 50 mm",
        "touchpoints": ["Inoculate seeds with rhizobium", "Avoid waterlogging", "Harvest when lower pods turn brown"],
        "image": "img/default_hero.jpg"
    },
    "cucumber": {
        "summary": "Cucumber grows fast in warm weather with fertile, well-drained soil and consistent moisture.",
        "ph": "6.0 - 7.0",
        "temperature": "20 - 30°C",
        "rainfall": "60 - 100 mm",
        "touchpoints": ["Provide trellis support", "Keep soil consistently moist", "Harvest frequently to encourage production"],
        "image": "img/default_hero.jpg"
    },
    "pumpkin": {
        "summary": "Pumpkin thrives in warm weather with rich, well-drained soil and plenty of space to spread.",
        "ph": "6.0 - 7.5",
        "temperature": "18 - 28°C",
        "rainfall": "60 - 100 mm",
        "touchpoints": ["Give plenty of space", "Water at base to avoid fungal disease", "Harvest when skin hardens"],
        "image": "img/default_hero.jpg"
    }
}

DEFAULT_CROP_INFO = {
    "summary": "The hero image will appear here once a crop recommendation is generated.",
    "ph": "N/A",
    "temperature": "N/A",
    "rainfall": "N/A",
    "touchpoints": ["Use local agronomy advice", "Monitor soil and climate closely", "Follow balanced nutrient management"],
    "image": "img/default_hero.jpg"
}

DEFAULT_HERO_IMAGE = "img/default_hero.jpg"

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

RADAR_MAX = {"N": 140, "P": 145, "K": 205, "temperature": 45, "humidity": 100, "ph": 14, "rainfall": 300}


def get_crop_insights(crop_name):
    return CROP_GUIDE.get(crop_name.lower(), DEFAULT_CROP_INFO)


def resolve_crop_image(crop_name):
    crop_info = get_crop_insights(crop_name)
    image_path = crop_info.get("image", DEFAULT_CROP_INFO["image"])
    result = image_path.replace("img/", "") if image_path else "default_hero.jpg"
    print(f"DEBUG: crop_name={crop_name}, image_path={image_path}, result={result}")
    return result


def train_and_save_model():
    data_path = os.path.join(os.path.dirname(__file__), "dataset.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Training dataset not found at {data_path}")

    df = pd.read_csv(data_path).dropna()
    X = df[FEATURE_COLUMNS]
    y = df["crop"]

    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)

    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    return model, scaler


def ensure_model_artifacts():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        train_and_save_model()


def load_model(path):
    ensure_model_artifacts()
    with open(path, "rb") as f:
        return pickle.load(f)


def preprocess_input(values, scaler):
    df = pd.DataFrame([values], columns=FEATURE_COLUMNS)
    df_scaled = scaler.transform(df)
    return df_scaled


@app.route("/", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "healthy", "service": "OPTI-CROP API"}, 200


@app.route("/api/image/<filename>")
@app.route("/image/<filename>")
def get_image(filename):
    try:
        img_dir = os.path.join(os.path.dirname(__file__), "static", "img")
        print(f"DEBUG IMAGE ROUTE: filename={filename}, img_dir={img_dir}")
        return send_from_directory(img_dir, filename)
    except Exception as e:
        print(f"DEBUG IMAGE ERROR: {str(e)}")
        return "File not found", 404


def calculate_match_score(radar_user, radar_ideal, radar_labels):
    diffs = [abs(radar_user[i] - radar_ideal[i]) for i in range(len(radar_labels))]
    avg_diff = sum(diffs) / len(diffs)
    
    if avg_diff <= 10:
        return "excellent", "Your field conditions are an excellent match for this crop. Go ahead and plant with confidence!", "success", "bi-check-circle-fill"
    elif avg_diff <= 20:
        return "good", "Your field is a good match. Minor adjustments may improve yield.", "primary", "bi-check-circle"
    else:
        return None, None, None, None


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


@app.route("/api/predict", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form or {}

    try:
        user_input = {col: float(data.get(col, 0)) for col in FEATURE_COLUMNS}
    except (ValueError, TypeError):
        return {"error": "Please enter valid numeric values for all fields."}, 400

    if any(value < 0 for value in user_input.values()):
        return {"error": "Please enter non-negative values for the input parameters."}, 400

    model = load_model(MODEL_PATH)
    scaler = load_model(SCALER_PATH)
    features = preprocess_input(user_input, scaler)
    proba = model.predict_proba(features)[0]
    
    radar_labels = FEATURE_COLUMNS
    top_indices = np.argsort(proba)[::-1]
    
    best_crop = model.classes_[top_indices[0]]
    ideal = CROP_IDEAL.get(best_crop.lower(), {})
    
    radar_user = [round(user_input[k] / RADAR_MAX[k] * 100, 1) for k in radar_labels]
    radar_ideal = [round(ideal.get(k, 0) / RADAR_MAX[k] * 100, 1) for k in radar_labels]
    
    match_status, match_message, match_color, match_icon = calculate_match_score(radar_user, radar_ideal, radar_labels)
    if not match_status:
        best_match_status = "best_available"
        best_match_message = "This is the best crop for your conditions among available options."
        best_match_color = "info"
        best_match_icon = "bi-info-circle-fill"
    else:
        best_match_status = match_status
        best_match_message = match_message
        best_match_color = match_color
        best_match_icon = match_icon

    best_param_advice = get_parameter_advice(radar_user, radar_ideal, radar_labels)
    
    crop_info = get_crop_insights(best_crop)
    crop_image = resolve_crop_image(best_crop)
    print(f"DEBUG: best_crop={best_crop}, crop_image={crop_image}")
    
    top3_indices = np.argsort(proba)[::-1][:3]
    top3 = [
        {"crop": model.classes_[i], "confidence": round(proba[i] * 100, 1)}
        for i in top3_indices
    ]
    
    return {
        "result": best_crop,
        "inputs": user_input,
        "hero_image": crop_image,
        "hero_crop": best_crop,
        "crop_image": crop_image,
        "crop_summary": crop_info["summary"],
        "crop_ph": crop_info["ph"],
        "crop_temperature": crop_info["temperature"],
        "crop_rainfall": crop_info["rainfall"],
        "crop_touchpoints": crop_info["touchpoints"],
        "top3": top3,
        "radar_labels": radar_labels,
        "radar_user": radar_user,
        "radar_ideal": radar_ideal,
        "match_status": best_match_status,
        "match_message": best_match_message,
        "match_color": best_match_color,
        "match_icon": best_match_icon,
        "param_advice": best_param_advice,
    }, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

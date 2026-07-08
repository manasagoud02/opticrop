# OPTI-CROP: Smart Agricultural Crop Recommendation System

This module provides a unified Flask application integrated with machine learning models trained on soil nutrients and climatic parameters to recommend crops.

## Quick Start

### 1. Configure the Environment & Dependencies
Ensure you are using Python 3.10+ (Python 3.14 was verified). Install all required packages:
```bash
pip install -r requirements.txt
```

### 2. Model Training & Comparison (KNN, Logistic Regression, Decision Tree, Random Forest, K-Means)
Train all five models, compare their accuracies, output visual diagnostic plots, and persist the best model (`RandomForestClassifier`) along with the feature scaler:
```bash
python compare_models.py
```
*Note: Diagnostic plots (accuracy comparison bar chart, confusion matrix, feature importance, K-Means PCA clusters) will be saved under `static/images/`.*

### 3. Start the Flask Application
Run the local development server:
```bash
python app.py
```
Once started, navigate to:
**`http://127.0.0.1:5000/`**

---

## Testing & Verification

Run the automated test suite verifying both the standalone model predictions and backend HTTP API endpoints:
```bash
python -m unittest discover -s tests
```

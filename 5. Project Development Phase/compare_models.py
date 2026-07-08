import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent GUI dialogs
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.decomposition import PCA

# Classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def load_and_preprocess_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Please copy it first.")
    
    # 1. Load data
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded successfully. Shape: {df.shape}")
    
    # 2. Clean data (check for and drop missing values)
    initial_len = len(df)
    df = df.dropna()
    dropped_count = initial_len - len(df)
    if dropped_count > 0:
        print(f"Dropped {dropped_count} rows with missing values.")
        
    X = df[FEATURE_COLUMNS]
    y = df["crop"]
    
    # 3. Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Train-Test Split (80/20 stratified split)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, scaler, X_scaled, y

def train_and_evaluate_models():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    X_train, X_test, y_train, y_test, scaler, X_all, y_all = load_and_preprocess_data()
    
    # Initialize models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    accuracies = {}
    classification_reports = {}
    trained_models = {}
    
    # 1. Train Classifiers
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        accuracies[name] = acc
        classification_reports[name] = classification_report(y_test, y_pred, output_dict=True)
        trained_models[name] = model
        print(f"{name} Test Accuracy: {acc:.4f}")
        
    # 2. K-Means Clustering Comparison
    # Since there are 42 unique crops in the dataset, we set n_clusters=42
    n_classes = len(y_all.unique())
    print(f"Training K-Means Clustering with {n_classes} clusters...")
    kmeans = KMeans(n_clusters=n_classes, random_state=42, n_init=10)
    kmeans.fit(X_train)
    
    # Map clusters to true classes by finding the most frequent class in each cluster
    cluster_labels = kmeans.labels_
    cluster_to_crop = {}
    for cluster in range(n_classes):
        indices = np.where(cluster_labels == cluster)[0]
        if len(indices) > 0:
            crops_in_cluster = y_train.iloc[indices]
            most_common = crops_in_cluster.mode()[0]
            cluster_to_crop[cluster] = most_common
        else:
            cluster_to_crop[cluster] = "unknown"
            
    # Evaluate K-Means as a classifier on test data
    test_clusters = kmeans.predict(X_test)
    kmeans_preds = [cluster_to_crop.get(c, "unknown") for c in test_clusters]
    kmeans_acc = accuracy_score(y_test, kmeans_preds)
    accuracies["K-Means Clustering"] = kmeans_acc
    print(f"K-Means Clustering Mapping Accuracy: {kmeans_acc:.4f}")
    
    # --- Visualizations ---
    # Plot 1: Model Accuracy Comparison
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    bar_data = pd.DataFrame({
        "Algorithm": list(accuracies.keys()),
        "Accuracy": [acc * 100 for acc in accuracies.values()]
    })
    ax = sns.barplot(x="Algorithm", y="Accuracy", data=bar_data, palette="viridis")
    plt.title("Model Accuracy Comparison", fontsize=16, fontweight='bold', pad=15)
    plt.ylabel("Accuracy (%)", fontsize=12)
    plt.xlabel("Algorithm", fontsize=12)
    plt.ylim(0, 105)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), 
                    ha='center', va='center', fontsize=10, color='black', 
                    fontweight='bold', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "model_accuracy_comparison.png"), dpi=150)
    plt.close()
    
    # Plot 2: Confusion Matrix for the Best Classifier (Random Forest)
    best_model_name = "Random Forest"
    best_model = trained_models[best_model_name]
    y_pred_best = best_model.predict(X_test)
    labels = sorted(list(y_test.unique()))
    cm = confusion_matrix(y_test, y_pred_best, labels=labels)
    
    plt.figure(figsize=(16, 14))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=labels, yticklabels=labels)
    plt.title(f"Confusion Matrix - {best_model_name}", fontsize=18, fontweight='bold', pad=20)
    plt.ylabel("True Crop Label", fontsize=14)
    plt.xlabel("Predicted Crop Label", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "confusion_matrix.png"), dpi=150)
    plt.close()
    
    # Plot 3: Feature Importance (Random Forest)
    plt.figure(figsize=(10, 6))
    importances = best_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    feature_ranking = [FEATURE_COLUMNS[i] for i in indices]
    
    sns.barplot(x=importances[indices] * 100, y=feature_ranking, palette="mako")
    plt.title("Random Forest - Feature Importance", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Importance Score (%)", fontsize=12)
    plt.ylabel("Soil/Environmental Parameter", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "feature_importance.png"), dpi=150)
    plt.close()
    
    # Plot 4: K-Means Clusters Visualized (PCA 2D Projection)
    plt.figure(figsize=(10, 8))
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_all)
    kmeans_full = KMeans(n_clusters=n_classes, random_state=42, n_init=10).fit(X_all)
    
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_full.labels_, cmap="tab20", s=25, alpha=0.8)
    plt.colorbar(scatter, label="Cluster ID")
    plt.title("K-Means Clustering Visualization (2D PCA)", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Principal Component 1", fontsize=12)
    plt.ylabel("Principal Component 2", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "kmeans_clusters.png"), dpi=150)
    plt.close()
    
    # Save the Best Model (Random Forest) and Scaler
    print(f"Saving the best model ({best_model_name}) to {MODEL_PATH}...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)
    print(f"Saving Scaler to {SCALER_PATH}...")
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
        
    print("\nTraining and Evaluation Complete! Plots saved under static/images/")
    return accuracies

if __name__ == "__main__":
    train_and_evaluate_models()

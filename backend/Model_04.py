import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def train_classifier_rf():
    # 1. Setup Paths
    base = 'backend/' if os.path.exists('backend/Datasets') else ''
    if not os.path.exists(os.path.join(base, 'Datasets')): base = '../backend/'
    
    DATA_FILE = os.path.join(base, "Datasets/master_data_model_04.csv")
    MODEL_OUT = os.path.join(base, "Models/model_classifier_rf.pkl")
    PLOT_OUT = os.path.join(base, "Datasets/classifier_matrix.png")
    
    print("Loading Master Dataset...")
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(" Error: Master file missing.")
        return

    df.columns = df.columns.str.strip().str.lower()

    # 2. Smart Column Finder
    def find_col(target, columns):
        for col in columns:
            if target in col: return col
        return None

    feature_map = {
        "labor": ["labor_intensity_score"],
        "mobility": ["mobility_index"],
        "infiltration": ["infiltration_index"],
        "weekend": ["is_weekend"]
    }
    
    final_features = []
    
    for key, search_terms in feature_map.items():
        found = False
        for term in search_terms:
            col = find_col(term, df.columns)
            if col:
                df[key] = df[col]
                final_features.append(key)
                found = True
                break
        if not found and key == "weekend": 
             df["weekend"] = 0
             final_features.append("weekend")

    # 3 Target Engineering
    enrol_col = find_col("enro", df.columns) 
    bio_col = find_col("bio_updates", df.columns) 
    if enrol_col is None: 
        print(" Warning: Could not find Enrolment column. using 'total_enro_updates' default.")
        enrol_col = 'total_enro_updates'
        
    print(f"Using columns: Enrolment='{enrol_col}', Biometric='{bio_col}'")
    
    df["performance_score"] = df[enrol_col].fillna(0) + df[bio_col].fillna(0) 

    # Smart Feature: Workload Efficiency 
    if "labor" in df.columns and "mobility" in df.columns:
        df["workload_efficiency"] = df["labor"] * (df["mobility"] + 1)
        final_features.append("workload_efficiency")

    # Define High Performer (Top 30%)
    threshold = df["performance_score"].quantile(0.70)
    df["is_high_performer"] = (df["performance_score"] >= threshold).astype(int)

    print(f"Features used: {final_features}")
    print(f"Target Distribution: {df['is_high_performer'].value_counts(normalize=True)}")

    # 4. Splitting for train and test
    X = df[final_features].fillna(0)
    y = df["is_high_performer"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Training Random Forest
    print("Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=500, 
        max_depth=25, 
        min_samples_split=10,
        max_features="sqrt",
        random_state=42,
        class_weight=None
    )

    model.fit(X_train, y_train)

    # 6. Evaluation
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)

    print(f"\n--- MODEL PERFORMANCE ---")
    print(f"Achieved Accuracy: {accuracy*100:.2f}%")
    print("\nDetailed Report:")
    print(classification_report(y_val, y_pred))

    # Feature Importance (Insights for  frontend dashboard)
    importances = pd.DataFrame({
        "Feature": final_features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("\nTop Performance Drivers:")
    print(importances)
    # 7. Saving (Crucial for Dashboard)
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    INSIGHTS_PATH = os.path.join(base, "Datasets/model_04_insights.csv")
    importances.to_csv(INSIGHTS_PATH, index=False)
    print(f" Insights Saved: {INSIGHTS_PATH}")
    # Save Matrix Plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion_matrix(y_val, y_pred), annot=True, fmt='d', cmap='Greens')
    plt.title(f'RF Classification (Acc: {accuracy:.2f})')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig(PLOT_OUT)
    
    print(f"\n Model Saved: {MODEL_OUT}")
    print(f" Confusion Matrix Saved: {PLOT_OUT}")
if __name__ == "__main__":
    train_classifier_rf()
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib
import os

def train_model_02():
    print("Loading datasets (Standard Mode)...")
    try:
        df_bio = pd.read_csv(r'Datasets\cleaned_data_set_biometric.csv')
        df_demo = pd.read_csv(r'Datasets\cleaned_data_set_demographic.csv')
    except FileNotFoundError:
        print(" Error: Original cleaned CSVs not found.")
        return
    df_merged = pd.merge(df_bio, df_demo, 
                         on=['date', 'state', 'district', 'pincode', 'is_weekend', 'month_name'], 
                         how='inner')
    df_merged.fillna(0, inplace=True)
    
    features = ['labor_intensity_score', 'mobility_index', 'child_compliance_ratio']
    X = df_merged[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train K=3 (this gave the most optimized score in our tests hehe)
    print("Training K-Means (K=3)...")
    best_model = KMeans(n_clusters=3, random_state=42, n_init=10)
    best_model.fit(X_scaled)
    df_merged['cluster_id'] = best_model.labels_ #clusters

    # Naming Logic
    def name_cluster(row):
        if row['mobility_index'] > row['labor_intensity_score']:
            return "Urban / Digital Hub"
        elif row['labor_intensity_score'] > 0.6:
            return "Manual Labor Zone"
        else:
            return "Evolving / Mixed"

    df_merged['cluster_name'] = df_merged.apply(name_cluster, axis=1)

    # Score
    score = silhouette_score(X_scaled, best_model.labels_, sample_size=10000)
    print(f" Final Silhouette Score: {score:.4f}")

    # Savin

    joblib.dump(best_model, r'Models\model_pulse_kmeans.pkl')
    joblib.dump(scaler, r'Models\model_pulse_scaler.pkl')
    
    # 2. Data for frontend's Dashboard
    output_cols = ['date', 'state', 'district', 'cluster_id', 'cluster_name'] + features
    df_merged[output_cols].to_csv(r'Datasets\scored_pulse_data.csv', index=False)
    
    print(" Files Saved: 'scored_pulse_data.csv', 'model_pulse_kmeans.pkl', 'model_pulse_scaler.pkl'")

if __name__ == "__main__":
    train_model_02()
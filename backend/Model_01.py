import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
CONTAMINATION_RATE = 0.03 
N_ESTIMATORS = 200
def train_model_01():
    df_enrol=pd.read_csv(r'Datasets\cleaned_data_set_enrolment.csv')
    df_demo=pd.read_csv(r'Datasets\cleaned_data_set_demographic.csv')
    df_merged = pd.merge(df_enrol, df_demo, 
                         on=['date', 'state', 'district', 'pincode', 'is_weekend', 'month_name'], 
                         how='inner')
    df_merged.fillna(0, inplace=True)
    features = [
        'infiltration_index',    # High adult enrolment = Suspicious
        'Birth_index',  # Low birth enrolment = Suspicious
        'correction_index'       # High child updates = Operator Incompetence
        ]
    X= df_merged[features]
    print(f"Training Model with {N_ESTIMATORS}trees")
    model=IsolationForest(n_estimators=N_ESTIMATORS,
                            contamination=CONTAMINATION_RATE,
                            random_state=42,
                            n_jobs=-1
        )
    model.fit(X)

    df_merged['raw_anomaly_score'] = model.decision_function(X)
    min_score = df_merged['raw_anomaly_score'].min()
    max_score = df_merged['raw_anomaly_score'].max()

    df_merged['risk_score'] = 100 * (max_score - df_merged['raw_anomaly_score']) / (max_score - min_score)
    df_merged['anomaly_label'] = model.predict(X)
    anomalies = df_merged[df_merged['anomaly_label'] == -1]

    print("\nMODEL RESULTS")
    print(f"Total Data Points: {len(df_merged)}")
    print(f"Anomalies Detected: {len(anomalies)} ({len(anomalies)/len(df_merged)*100:.2f}%)")
    
    print("\nTOP 5 HIGH RISK DISTRICTS")
    print(anomalies[['district', 'risk_score', 'infiltration_index']].sort_values(by='risk_score', ascending=False).head(5))

    def print_model_health(df, features):
        print("\n--- MODEL HEALTH REPORT ---")
        sample = df.sample(min(10000, len(df)), random_state=42)
        sil_score = silhouette_score(sample[features], sample['anomaly_label'])
        print(f"Silhouette Score: {sil_score:.4f} (Valid range for Anomaly Detection: 0.4 - 0.7)")

        anomalies = df[df['anomaly_label'] == -1]
        normals = df[df['anomaly_label'] == 1]
        
        bad_avg = anomalies['infiltration_index'].mean()
        good_avg = normals['infiltration_index'].mean()
        contrast = bad_avg / (good_avg + 0.0001) 
        
        print(f"Contrast Ratio: {contrast:.2f}x")
        print(f"   - Normal Districts Avg Adult Enrolment: {good_avg*100:.1f}%")
        print(f"   - Flagged Districts Avg Adult Enrolment: {bad_avg*100:.1f}%")
        if contrast > 2.0:
            print(" SUCCESS: The model is finding significantly distinct anomalies.")
            joblib.dump(model, 'Models/model_sentinel.pkl')
            print("\nSaving processed data to 'anomalies_data.csv'...")
            df_merged.to_csv('Datasets/anomalies_data.csv', index=False)
            print("Save complete.")

        else:
            print(" WARNING: The flagged anomalies look too similar to normal data.")
    print_model_health(df_merged, features)

if __name__ == "__main__":
    train_model_01()
    
import os
import json
import joblib
import pandas as pd
import numpy as np
import random
import hashlib
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from report import generate_ai_report 

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

#paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Datasets")
MODEL_DIR = os.path.join(BASE_DIR, "Models")

#Cache
MODELS = {}
DATA = {}
REPORT_CACHE = {"timestamp": 0, "data": None}
CACHE_DURATION = 3600

STATE_CENTERS = {
    "Uttar Pradesh": {"lat": 26.8467, "lng": 80.9462},
    "Maharashtra": {"lat": 19.7515, "lng": 75.7139},
    "Karnataka": {"lat": 15.3173, "lng": 75.7139},
    "Delhi": {"lat": 28.7041, "lng": 77.1025},
    "Tamil Nadu": {"lat": 11.1271, "lng": 78.6569},
    "Gujarat": {"lat": 22.2587, "lng": 71.1924},
    "West Bengal": {"lat": 22.9868, "lng": 87.8550},
    "Rajasthan": {"lat": 27.0238, "lng": 74.2179},
    "Bihar": {"lat": 25.0961, "lng": 85.3131},
    "Madhya Pradesh": {"lat": 22.9734, "lng": 78.6569},
    "DEFAULT": {"lat": 20.5937, "lng": 78.9629}
}

def jitter(value): 
    return value + random.uniform(-0.15, 0.15)

def get_smart_coords(state, district):
    """
    Deterministically generates coordinates for a district near its state center 
    using a hash of the district name, so the map pins stay consistent.
    """
    dist_str = str(district)
    base = STATE_CENTERS.get(state, STATE_CENTERS["DEFAULT"])
    h = int(hashlib.md5(dist_str.encode()).hexdigest(), 16)
    return {
        "lat": base["lat"] + ((h % 1000)/1000.0 * 3.0 - 1.5),
        "lng": base["lng"] + (((h // 1000)%1000)/1000.0 * 3.0 - 1.5)
    }
def load_resources():
    print("Loading Static Datasets...")
    try:
        if os.path.exists(os.path.join(DATA_DIR, "forecast_data.csv")):
            DATA["forecast"] = pd.read_csv(os.path.join(DATA_DIR, "forecast_data.csv"))
        if os.path.exists(os.path.join(DATA_DIR, "scored_pulse_data.csv")):
            DATA["clusters"] = pd.read_csv(os.path.join(DATA_DIR, "scored_pulse_data.csv"))
        if os.path.exists(os.path.join(DATA_DIR, "model_04_insights.csv")):
            DATA["insights"] = pd.read_csv(os.path.join(DATA_DIR, "model_04_insights.csv"))
        if os.path.exists(os.path.join(DATA_DIR, "anomalies_data.csv")):
            DATA["anomalies"] = pd.read_csv(os.path.join(DATA_DIR, "anomalies_data.csv"))
        print(" Resources Loaded Successfully.")
    except Exception as e:
        print(f" Error Loading Resources: {e}")

def load_models():
    if not MODELS:
        print("Loading AI Models into Memory...")
        try:
            MODELS['sentinel'] = joblib.load(os.path.join(MODEL_DIR, 'model_sentinel.pkl'))
            MODELS['pulse'] = joblib.load(os.path.join(MODEL_DIR, 'model_pulse_kmeans.pkl'))
            MODELS['scaler'] = joblib.load(os.path.join(MODEL_DIR, 'model_pulse_scaler.pkl'))
            MODELS['forecast_xgb'] = joblib.load(os.path.join(MODEL_DIR, 'footfall_forecast_xgb.pkl'))
            MODELS['forecast_rf'] = joblib.load(os.path.join(MODEL_DIR, 'footfall_forecast_rf.pkl'))
            MODELS['classifier'] = joblib.load(os.path.join(MODEL_DIR, 'model_classifier_rf.pkl'))
            
            print("All Models Loaded Successfully.")
        except Exception as e:
            print(f"CRITICAL WARNING: Could not load some models. {e}")

load_resources()

# API ENDPOINTS

@app.route("/", methods=["GET"])
def health(): 
    return jsonify({"status": "online", "models_loaded": len(MODELS) > 0})

# 1. Forecast data (Graph)
@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    if 'forecast' not in DATA: return jsonify([]), 404
    df = DATA['forecast'].rename(columns={'target_trend':'Actual', 'predicted_trend':'Predicted'})
    return jsonify(df[['date','Actual','Predicted']].dropna().tail(60).to_dict(orient='records'))
    #last ke 60 days return kre hain for cleaner data

# 2. Cluster map (Model 2)
@app.route("/api/clusters", methods=["GET"])
def get_clusters():
    if "clusters" not in DATA: return jsonify([])
    # Sample to avoid overloading the frontend map
    df = DATA["clusters"].sample(min(len(DATA["clusters"]), 5000), random_state=42)
    points = []
    for _, row in df.iterrows():
        c = get_smart_coords(str(row.get("state")), str(row.get("district")))
        points.append({
            "lat": jitter(c["lat"]), 
            "lng": jitter(c["lng"]),
            "cluster_name": row.get("cluster_name"),
            "intensity": row.get("labor_intensity_score"),
            "district": row.get("district")
        })
    return jsonify(points)

# 3. Insights (Model 4 Feature Importance)
@app.route("/api/insights", methods=["GET"])
def get_insights():
    if "insights" not in DATA: return jsonify([])
    return jsonify(DATA["insights"].rename(columns={"Feature":"feature", "Importance":"importance"}).to_dict(orient="records"))

# 4. Anomaly heatmap(Model 1)
@app.route("/api/anomalies", methods=["GET"])
def get_anomalies():
    if "anomalies" not in DATA: return jsonify([])
    df = DATA["anomalies"]
    anomalies = df[
        (df["anomaly_label"] == -1) & 
        (df["risk_score"] > 60.00)
    ].sample(min(len(df), 500), random_state=42)
    
    alerts = []
    for _, row in anomalies.iterrows():
        state = str(row.get("state", "Uttar Pradesh"))
        district = str(row.get("district", "Unknown"))
        center = get_smart_coords(state, district)
        alerts.append({
            "lat": jitter(center["lat"]),
            "lng": jitter(center["lng"]),
            "score": float(row.get("risk_score", 0)),
            "district": district,
            "state": state
        })
    return jsonify(alerts)

# 5. GENERATE REPORT (LLM abhi ke liye gemini hi h, Fine tuned LLM abhi configure nhi hua h pura
@app.route("/api/generate_report", methods=["GET"])
def generate_report_route():
    global REPORT_CACHE
    current_time = time.time()
    
    # Check Cache
    if REPORT_CACHE["data"] and (current_time - REPORT_CACHE["timestamp"] < CACHE_DURATION):
        print(f" Serving Report from Cache (Expires in {int(CACHE_DURATION - (current_time - REPORT_CACHE['timestamp']))}s)")
        return jsonify(REPORT_CACHE["data"])
    
    if "clusters" not in DATA or "anomalies" not in DATA: 
        return jsonify({"error": "Data not available"}), 500

    try:
        df_clusters = DATA["clusters"]
        df_anomalies = DATA["anomalies"]
        
        avg_labor = df_clusters["labor_intensity_score"].mean()
        high_risk_count = len(df_anomalies[df_anomalies["anomaly_label"] == -1])
        avg_risk = df_anomalies["risk_score"].mean()
        
        stats = (
            f"Analyzed {len(df_clusters)} districts across India. "
            f"Average Labor Intensity is {avg_labor:.2f}. "
            f"Average Risk Score is {avg_risk:.2f}. "
            f"Total High Risk Zones identified: {high_risk_count}."
        )
        report = generate_ai_report(stats)
        
        response_data = {"report": report, "summary": stats}
        REPORT_CACHE = {
            "timestamp": current_time,
            "data": response_data
        }   
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6. LIVE SIMULATION
@app.route("/api/simulate", methods=["POST"])
def simulate_performance():
    load_models() 
    try:
        if 'file' not in request.files: 
            return jsonify({"error": "No file detected"}), 400
        file = request.files['file']
        
        # 2. Reading and cleaning
        raw_df = pd.read_csv(file)
        raw_df.columns = [c.strip().lower() for c in raw_df.columns]
        results_df = raw_df.copy()
        
        # Helper function for 
        def get_col(df, names, default=0):
            for name in names:
                if name in df.columns: return df[name].fillna(default)
            return pd.Series([default]*len(df))

        #Model 01
        features_m1 = ['infiltration_index', 'birth_index', 'correction_index']
        X_anom = pd.DataFrame({
            'infiltration_index': get_col(raw_df, ['infiltration_index', 'infiltration']),
            'Birth_index': get_col(raw_df, ['birth_index', 'births', 'birth']),
            'correction_index': get_col(raw_df, ['correction_index', 'correction', 'updates'])
        })
        
        if 'sentinel' in MODELS:
            raw_scores = MODELS['sentinel'].decision_function(X_anom)
            # Normalized scores
            results_df['risk_score'] = np.round(100 * (raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min() + 1e-6), 2)
            results_df['is_anomaly'] = MODELS['sentinel'].predict(X_anom)
            results_df['anomaly_status'] = np.where(results_df['is_anomaly'] == -1, "High Risk", "Normal")

        # Model02
        X_clus = pd.DataFrame({
            'labor_intensity_score': get_col(raw_df, ['labor_intensity_score', 'labor']),
            'mobility_index': get_col(raw_df, ['mobility_index', 'mobility']),
            'child_compliance_ratio': get_col(raw_df, ['child_compliance_ratio', 'child_compliance'])
        })
        
        if 'pulse' in MODELS and 'scaler' in MODELS:
            X_clus_scaled = MODELS['scaler'].transform(X_clus)
            results_df['cluster_id'] = MODELS['pulse'].predict(X_clus_scaled)
            
            def get_cluster_name(row):
                if row['mobility_index'] > row['labor_intensity_score']: return "Urban / Digital Hub"
                elif row['labor_intensity_score'] > 0.6: return "Manual Labor Zone"
                else: return "Evolving / Mixed"
            
            results_df['cluster_name'] = X_clus.apply(get_cluster_name, axis=1)

        # --- model03 
        if 'forecast_xgb' in MODELS and 'forecast_rf' in MODELS:
            # Prepare Time Features
            if 'date' in raw_df.columns:
                dates = pd.to_datetime(raw_df['date'])
                day_sin = np.sin(2 * np.pi * dates.dt.dayofweek / 7)
                day_cos = np.cos(2 * np.pi * dates.dt.dayofweek / 7)
                month_sin = np.sin(2 * np.pi * dates.dt.month / 12)
                month_cos = np.cos(2 * np.pi * dates.dt.month / 12)
            else:
                day_sin, day_cos, month_sin, month_cos = 0, 0, 0, 0
                
            trend = get_col(raw_df, ['target_trend', 'total_enrolment'], 0)
            X_fore = pd.DataFrame({
                "is_weekend": get_col(raw_df, ['is_weekend'], 0),
                "lag_1": trend, "lag_7": trend, 
                "momentum": 1.0, "volatility": 0.0,
                "day_sin": day_sin, "day_cos": day_cos,
                "month_sin": month_sin, "month_cos": month_cos
            })
            
            pred_log_xgb = MODELS['forecast_xgb'].predict(X_fore)
            pred_log_rf = MODELS['forecast_rf'].predict(X_fore)
            pred_log_final = (0.6 * pred_log_xgb) + (0.4 * pred_log_rf)
            results_df['forecasted_footfall'] = np.round(np.expm1(pred_log_final), 2)

        # model 04 
        # --- MODEL 4: CLASSIFIER ---
        if 'classifier' in MODELS:
            labor = get_col(raw_df, ['labor_intensity_score', 'labor'])
            mobility = get_col(raw_df, ['mobility_index', 'mobility'])
            efficiency = labor * (mobility + 1)
            
            X_class = pd.DataFrame({
                "labor": labor,                
                "mobility": mobility,           
                "infiltration": get_col(raw_df, ['infiltration_index', 'infiltration']), 
                "weekend": get_col(raw_df, ['is_weekend'], 0),
                "workload_efficiency": efficiency
            })
            X_class.fillna(0, inplace=True)
            
            probs = MODELS['classifier'].predict_proba(X_class)[:, 1]
            results_df['success_probability'] = np.round(probs * 100, 2)
            results_df['performance_label'] = np.where(probs > 0.65, "High Performer", "Needs Improvement")
        
        # 1. Map Data: Anomalies Only
        anomalies_map = []
        for _, row in results_df[results_df['anomaly_status'] == 'High Risk'].iterrows():
            coords = get_smart_coords(str(row.get('state', 'DEFAULT')), str(row.get('district', 'Unknown')))
            anomalies_map.append({
                "lat": jitter(coords["lat"]),
                "lng": jitter(coords["lng"]),
                "district": row.get('district', 'Unknown'),
                "risk_score": float(row.get('risk_score', 0)),
                "state": row.get('state', 'Unknown')
            })

        # 2. Map Data: Clusters Only
        clusters_map = []
        for _, row in results_df.iterrows():
            coords = get_smart_coords(str(row.get('state', 'DEFAULT')), str(row.get('district', 'Unknown')))
            clusters_map.append({
                "lat": jitter(coords["lat"]),
                "lng": jitter(coords["lng"]),
                "district": row.get('district', 'Unknown'),
                "cluster_name": row.get('cluster_name', 'Unknown'),
                "labor_intensity": float(row.get('labor_intensity_score', 0))
            })

        # 3. Generating Report
        avg_success = results_df.get('success_probability', pd.Series([0])).mean()
        high_risk_count = len(results_df[results_df['anomaly_status'] == 'High Risk'])
        forecast_avg = results_df.get('forecasted_footfall', pd.Series([0])).mean()

        #the context string for the LLM
        stats_context = (
            f"Simulated {len(results_df)} districts. "
            f"Average Success Probability: {avg_success:.2f}%. "
            f"High Risk Anomalies Detected: {high_risk_count}. "
            f"Projected Footfall Avg: {forecast_avg:.0f}."
        )
        ai_report_string = generate_ai_report(stats_context)

        # 4. Final response 
        response_payload = {
            # Main data for tables/graphs (includes success_probability, forecasted_footfall)
            "predictions": results_df.replace({np.nan: None}).to_dict(orient='records'),
            # Map 1 Data
            "anomalies_map": anomalies_map,
            # Map 2 Data
            "clusters_map": clusters_map,
            # String for the Report Section
            "report": ai_report_string,
            "status": "success"
        }

        print(f"Success: Processed {len(results_df)} rows. Sending {len(anomalies_map)} anomalies and {len(clusters_map)} cluster points.")
        return jsonify(response_payload)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": f"Simulation Failed: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(debug=True, port=5000)
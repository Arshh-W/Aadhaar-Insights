import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
import joblib
import os

#configurations for model training(Akarsh arsh ke customers ko sambhaal kr run kriyo, mai hang hua toh mujhe mt kehna)
N_ESTIMATORS = 600     
LEARNING_RATE = 0.005  
MAX_DEPTH = 5          
SUBSAMPLE = 0.8        
COLSAMPLE_BYTREE = 0.8 

def get_paths():#handling paths
    if os.path.exists('Datasets'): base = ''
    elif os.path.exists('backend/Datasets'): base = 'backend/'
    else: base = '../backend/' 
    return {
        'enrol': os.path.join(base, 'Datasets', 'cleaned_data_set_enrolment.csv'),
        'demo': os.path.join(base, 'Datasets', 'cleaned_data_set_demographic.csv'),
        'bio': os.path.join(base, 'Datasets', 'cleaned_data_set_biometric.csv'),
        'model_out': os.path.join(base, 'Models', 'footfall_forecast_xgb.pkl')
    }

def train_footfall_model():#training the model
    paths = get_paths()
    print("Loading datasets...")
    try:
        df_enrol = pd.read_csv(paths['enrol'])
        df_demo = pd.read_csv(paths['demo'])
        df_bio = pd.read_csv(paths['bio'])
    except FileNotFoundError:
        print(" Error: Datasets not found.")
        return

    print("Merging and Engineering Features...")#merge
    df = (
        df_enrol
        .merge(df_demo, on=["date", "state", "district", "pincode", "is_weekend", "month_name"], how="inner")
        .merge(df_bio, on=["date", "state", "district", "pincode", "is_weekend", "month_name"], how="inner")
    )
    df["date"] = pd.to_datetime(df["date"])

    enrol_col = 'total_enrolment' if 'total_enrolment' in df.columns else 'total_enro_updates'
    df["raw_footfall"] = df[enrol_col] + df["total_bio_updates"] + df["total_demo_updates"]
    #aggregate 
    daily = df.groupby("date").agg(
        raw_footfall=("raw_footfall", "sum"),
        is_weekend=("is_weekend", "max")
    ).reset_index().sort_values("date")

    # 1. Target Trend
    daily["target_trend"] = daily["raw_footfall"].rolling(window=7, min_periods=1).mean()

    # Features engineering
    daily["lag_1"] = daily["target_trend"].shift(1)
    daily["lag_7"] = daily["target_trend"].shift(7)
    daily["momentum"] = daily["lag_1"] / (daily["lag_7"] + 1e-6)
    daily["volatility"] = daily["target_trend"].rolling(7).std().fillna(0)
    
    # Cyclical Time(iska idea toh pura pura book se utha liya lolaa)
    daily['day_sin'] = np.sin(2 * np.pi * daily['date'].dt.dayofweek / 7)
    daily['day_cos'] = np.cos(2 * np.pi * daily['date'].dt.dayofweek / 7)
    daily['month_sin'] = np.sin(2 * np.pi * daily['date'].dt.month / 12)
    daily['month_cos'] = np.cos(2 * np.pi * daily['date'].dt.month / 12)

    daily.dropna(inplace=True)

    FEATURES = [#Finalizes features for training
        "is_weekend", "lag_1", "lag_7", "momentum", "volatility",
        "day_sin", "day_cos", "month_sin", "month_cos"
    ]
    TARGET = "target_trend"

    X = daily[FEATURES]
    y = daily[TARGET]
#training and validation sets split krdiye
    split = int(len(X) * 0.85)
    X_train, y_train = X.iloc[:split], y.iloc[:split]
    X_val, y_val = X.iloc[split:], y.iloc[split:]

    print(f"Training Ensemble on {len(X_train)} days...")

    # Log Transform(ye idea ke liye gemini ko thanks!)
    y_train_log = np.log1p(y_train)

    # XGBoost
    model_xgb = XGBRegressor(
        n_estimators=N_ESTIMATORS,
        learning_rate=LEARNING_RATE,
        max_depth=MAX_DEPTH,
        subsample=SUBSAMPLE,
        colsample_bytree=COLSAMPLE_BYTREE,
        random_state=42,
        n_jobs=-1
    )
    model_xgb.fit(X_train, y_train_log)
    preds_log_xgb = model_xgb.predict(X_val)

    # Random Forest(ye wale idea ke liye mujhe thankss hehe)
    model_rf = RandomForestRegressor(n_estimators=200, random_state=42)
    model_rf.fit(X_train, y_train_log)
    preds_log_rf = model_rf.predict(X_val)

    #Averaging the model outputs for optimized output heheh
    pred_log_final = (0.6 * preds_log_xgb) + (0.4 * preds_log_rf)
    
    pred = np.expm1(pred_log_final) 

    mape = mean_absolute_percentage_error(y_val, pred) * 100

    print("\n MODEL PERFORMANCE (XGBoost + Random Forest)")
    print(f"MAPE : {mape:.2f}%")
    #saving the xgboost model.
    os.makedirs(os.path.dirname(paths['model_out']), exist_ok=True)
    joblib.dump(model_xgb, paths['model_out'])
    
    daily['predicted_trend'] = np.nan
    daily.iloc[split:, daily.columns.get_loc('predicted_trend')] = pred
    #saving the forecast data for frontend
    output_path = os.path.join(os.path.dirname(paths['model_out']), '../Datasets/forecast_data.csv')
    daily.to_csv(output_path, index=False)
    print(f"Saved forecast data to {output_path}")

if __name__ == "__main__":
    train_footfall_model()
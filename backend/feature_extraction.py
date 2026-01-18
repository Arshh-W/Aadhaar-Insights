import pandas as pd
import numpy as np


def extract_features_from_csv(df, mapping):
    """
    EXTREMELY ROBUST: Ensures no rows are dropped and features are always valid.
    """
    try:
        # Create a fresh features dataframe with the same number of rows as input
        features = pd.DataFrame(index=df.index)

        # 1. Map values and force them to be numbers. 
        # If the column name in mapping is wrong, it uses 0.0 instead of crashing.
        for target, csv_col in mapping.items():
            if csv_col in df.columns:
                features[target] = pd.to_numeric(df[csv_col], errors='coerce').fillna(0.0)
            else:
                features[target] = 0.0

        # 2. Ensure all 5 required features exist (fill with 0 if missing from mapping)
        required = ['labor', 'mobility', 'infiltration', 'weekend']
        for req in required:
            if req not in features.columns:
                features[req] = 0.0

        # 3. Handle the Date/Weekend logic specifically
        # Check if the user mapped 'weekend' to a date column like 'record_date'
        weekend_col_name = mapping.get('weekend')
        if weekend_col_name in df.columns:
            try:
                dates = pd.to_datetime(df[weekend_col_name], errors='coerce')
                features['weekend'] = dates.dt.dayofweek.apply(lambda x: 1.0 if x >= 5 else 0.0).fillna(0.0)
            except:
                features['weekend'] = 0.0

        # 4. Calculate Workload Efficiency
        features['workload_efficiency'] = features['labor'] * (features['mobility'] + 1.0)

        # 5. Final check: Order must match your Random Forest Model
        model_inputs = features[['labor', 'mobility', 'infiltration', 'weekend', 'workload_efficiency']]
        
        # NEVER drop rows. If a value is missing, it's just 0.
        return df, model_inputs.fillna(0.0)

    except Exception as e:
        print(f"Extraction failed: {e}")
        raise ValueError(f"Feature Extraction Error: {str(e)}")
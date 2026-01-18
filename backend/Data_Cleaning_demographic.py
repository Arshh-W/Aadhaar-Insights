import pandas as pd
import numpy as np
import glob

# --- Load Data ---
file_pattern = r"backend\Datasets\api_data_aadhar_demographic\api_data_aadhar_demographic_*.csv" 
all_files = glob.glob(file_pattern)

if not all_files:
    print("WARNING: No files found!")
else:
    df_list = [pd.read_csv(f) for f in all_files]
    df_demo = pd.concat(df_list, ignore_index=True)

    # Cleaning
    df_demo.columns = df_demo.columns.str.strip().str.lower()
    df_demo['date'] = pd.to_datetime(df_demo['date'], format='%d-%m-%Y', errors='coerce')

    def standardize_text(text):
        if pd.isna(text): return "Unknown"
        return str(text).lower().strip().replace('&', 'and').title()

    df_demo['state'] = df_demo['state'].apply(standardize_text)
    df_demo['district'] = df_demo['district'].apply(standardize_text)
    
    cols_to_fill = ['demo_age_5_17', 'demo_age_17_']
    df_demo[cols_to_fill] = df_demo[cols_to_fill].fillna(0)

    #Feature Engineering

    # Feature 1: Total Volume
    df_demo['total_demo_updates'] = df_demo['demo_age_5_17'] + df_demo['demo_age_17_']

    # Feature 2: Mobility Index (Adult Dominance)
    df_demo['mobility_index'] = np.where(df_demo['total_demo_updates'] > 0,
                                         df_demo['demo_age_17_'] / df_demo['total_demo_updates'], 0)

    # Feature 3: Correction Index (Child Share)
    df_demo['correction_index'] = np.where(df_demo['total_demo_updates'] > 0,
                                           df_demo['demo_age_5_17'] / df_demo['total_demo_updates'], 0)

    # Feature 4: is week
    df_demo['is_weekend'] = df_demo['date'].dt.dayofweek.isin([5, 6]).astype(int)
    df_demo['month_name'] = df_demo['date'].dt.month_name()

    # --- Save ---
    output_path = r'backend\Datasets\cleaned_data_set_demographic.csv'
    df_demo.to_csv(output_path, index=False)
    
    print(f"Success! Processed {len(df_demo)} rows.")
    print(df_demo[['district', 'total_demo_updates', 'mobility_index', 'correction_index']].head())
import pandas as pd
import numpy as np
import glob

file_pattern = r"backend\Datasets\api_data_aadhar_enrolment\api_data_aadhar_enrolment_*.csv" 
all_files = glob.glob(file_pattern)

if not all_files:
    print("WARNING: No files found!")
else:
    df_list = [pd.read_csv(f) for f in all_files]
    df_enro = pd.concat(df_list, ignore_index=True)

    # Cleaning
    df_enro.columns = df_enro.columns.str.strip().str.lower()
    df_enro['date'] = pd.to_datetime(df_enro['date'], format='%d-%m-%Y', errors='coerce')

    def standardize_text(text):
        if pd.isna(text): return "Unknown"
        return str(text).lower().strip().replace('&', 'and').title()

    df_enro['state'] = df_enro['state'].apply(standardize_text)
    df_enro['district'] = df_enro['district'].apply(standardize_text)
    
    cols_to_fill = ['age_0_5', 'age_5_17','age_18_greater']
    df_enro[cols_to_fill] = df_enro[cols_to_fill].fillna(0)

    #Feature Engineering

    # Feature 1: Total enro Volume
    df_enro['total_enro_updates'] = df_enro['age_0_5']+ df_enro['age_5_17'] + df_enro['age_18_greater']

    # Feature 2: Infiltration (Adult Enrolment Ratio)
    df_enro['infiltration_index'] = np.where(df_enro['total_enro_updates'] > 0,
                                         df_enro['age_18_greater'] / df_enro['total_enro_updates'], 0)

    # Feature 3: Birth Rate (Child Enrolment Ratio)
    df_enro['Birth_index'] = np.where(df_enro['total_enro_updates'] > 0,
                                           df_enro['age_0_5'] / df_enro['total_enro_updates'], 0)

    #Feature 4: School Index(bachche mann ke sachche ratio)
    df_enro['School_Index']=np.where(df_enro['total_enro_updates']>0,
                                        df_enro['age_5_17']/df_enro['total_enro_updates'], 0)

    # Feature 4: is week
    df_enro['is_weekend'] = df_enro['date'].dt.dayofweek.isin([5, 6]).astype(int)
    df_enro['month_name'] = df_enro['date'].dt.month_name()


    output_path = r'backend\Datasets\cleaned_data_set_enrolment.csv'
    df_enro.to_csv(output_path, index=False)
    
    print(f"Success! Processed {len(df_enro)} rows.")
    print(df_enro[['district', 'total_enro_updates', 'infiltration_index', 'Birth_index','School_Index']].head())
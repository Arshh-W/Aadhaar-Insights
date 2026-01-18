import pandas as pd
import numpy as np
import glob

file_pattern = r"backend\Datasets\api_data_aadhar_biometric\api_data_aadhar_biometric_*.csv" 
all_files = glob.glob(file_pattern) #TO TRACK PATTERNS in bulk 
df_list = []
for filename in all_files:
    temp_df = pd.read_csv(filename)     
    df_list.append(temp_df)
#complete frame 
df_bio = pd.concat(df_list, ignore_index=True)

# Data cleaning 

# Cleaning Column Names (Removing spaces, lowercase)
df_bio.columns = df_bio.columns.str.strip().str.lower()

# 2. Convert Date to be in the correct format 
df_bio['date'] = pd.to_datetime(df_bio['date'], format='%d-%m-%Y', errors='coerce')

def standardize_text(text):
    if pd.isna(text): return "Unknown"
    text = str(text).lower().strip()
    text = text.replace('&', 'and') # normalize and signs to and
    return text.title() # Return to Title Case after editing

df_bio['state'] = df_bio['state'].apply(standardize_text)
df_bio['district'] = df_bio['district'].apply(standardize_text)

#Handling Missing Values
# Filling numeric NaNs with 0
cols_to_fill = ['bio_age_5_17', 'bio_age_17_']
df_bio[cols_to_fill] = df_bio[cols_to_fill].fillna(0)

# Feature Engineering and making aggregated fields

# Feature 1: Total Activity Volume
df_bio['total_bio_updates'] = df_bio['bio_age_5_17'] + df_bio['bio_age_17_']

# Feature 2: Child Compliance Ratio (Policy Metric)
# How many updates are for mandatory child updates vs adults?
df_bio['child_compliance_ratio'] = df_bio['bio_age_5_17'] / (df_bio['total_bio_updates'] + 0.0001)

# Feature 3: Labor Intensity Score (Socio economic metric)
# High adult biometric updates often indicate manual labor (faded fingerprints)
df_bio['labor_intensity_score'] = df_bio['bio_age_17_'] / (df_bio['total_bio_updates'] + 0.0001)

# Feature 4: Weekend Flag (Workforce Behavior)
# 1 if Saturday(5) or Sunday(6), else 0
df_bio['is_weekend'] = df_bio['date'].dt.dayofweek.isin([5, 6]).astype(int)

# Feature 5: Month Name (For Seasonality Analysis)
df_bio['month_name'] = df_bio['date'].dt.month_name()

print(f"Total Rows Processed: {len(df_bio)}")
print(df_bio.head())

#saving cleaned dataset(will do if cleaned dataset looks good enough)
df_bio.to_csv('backend\Datasets\cleaned_data_set_biometric.csv', index=False)

print("Success ahh!")
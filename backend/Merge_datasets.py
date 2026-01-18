import pandas as pd
import os

def merge_datasets():
    base = 'backend/' if os.path.exists('backend/Datasets') else ''
    if not os.path.exists(os.path.join(base, 'Datasets')): base = '../backend/'
    
    paths = {
        'enrol': os.path.join(base, 'Datasets', 'cleaned_data_set_enrolment.csv'),
        'demo': os.path.join(base, 'Datasets', 'cleaned_data_set_demographic.csv'),
        'bio': os.path.join(base, 'Datasets', 'cleaned_data_set_biometric.csv'),
        'output': os.path.join(base, 'Datasets', 'master_data_model_04.csv')
    }

    print("Loading datasets...")
    try:
        df_enrol = pd.read_csv(paths['enrol'])
        df_demo = pd.read_csv(paths['demo'])
        df_bio = pd.read_csv(paths['bio'])
    except FileNotFoundError:
        print(" Error: One or more input CSVs are missing.")
        return
    print("Merging Enrolment + Demographic...")
    merge_keys = ['date', 'state', 'district', 'pincode', 'is_weekend', 'month_name']
    
    df_merged = pd.merge(df_enrol, df_demo, on=merge_keys, how='inner')
    
    print("Merging + Biometric...")
    df_final = pd.merge(df_merged, df_bio, on=merge_keys, how='inner')

    df_final.fillna(0, inplace=True)

    # 4. Save
    df_final.to_csv(paths['output'], index=False)
    
    print("\n SUCCESS!")
    print(f"Merged File Saved: {paths['output']}")
    print(f"Total Rows: {len(df_final)}")
    print(f"Columns: {list(df_final.columns)}")

if __name__ == "__main__":
    merge_datasets()
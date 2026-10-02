import pandas as pd
import os

def save_parquet(**kwargs):
    ti = kwargs['ti']
    
    df_2018_json = ti.xcom_pull(task_ids='shuffle_data', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='shuffle_data', key='df_2019_clean')

    if df_2018_json is None or df_2019_json is None:
        raise ValueError("No data found after processing.")

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    output_folder = "~Output/"
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    df_2018.to_parquet(os.path.join(output_folder, "cleaned_medicare_data_2018.parquet"), index=False)
    df_2019.to_parquet(os.path.join(output_folder, "cleaned_medicare_data_2019.parquet"), index=False)

    print("Parquet files saved successfully.")

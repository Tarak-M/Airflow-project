import pandas as pd

def drop_duplicates(**kwargs):
    ti = kwargs['ti']
    df_2018_json = ti.xcom_pull(task_ids='load_data', key='df_2018')
    df_2019_json = ti.xcom_pull(task_ids='load_data', key='df_2019')

    if df_2018_json is None or df_2019_json is None:
        raise ValueError("No data found for df_2018 or df_2019")

    # Convert JSON back to DataFrame
    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    df_2018.drop_duplicates(inplace=True)
    df_2019.drop_duplicates(inplace=True)

    print("Duplicates removed.")

    # Push cleaned data back
    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

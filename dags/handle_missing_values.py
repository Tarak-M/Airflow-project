import pandas as pd

def handle_missing_values(**kwargs):
    ti = kwargs['ti']
    df_2018_json = ti.xcom_pull(task_ids='drop_duplicates', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='drop_duplicates', key='df_2019_clean')

    if df_2018_json is None or df_2019_json is None:
        raise ValueError("No data found after duplicate removal.")

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    df_2018.fillna(method="ffill", inplace=True)
    df_2019.fillna(method="ffill", inplace=True)

    print("Missing values handled.")

    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

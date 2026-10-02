import pandas as pd

def standardize_columns(**kwargs):
    ti = kwargs['ti']
    df_2018_json = ti.xcom_pull(task_ids='handle_missing_values', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='handle_missing_values', key='df_2019_clean')

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    df_2018.columns = [col.lower().replace(" ", "_") for col in df_2018.columns]
    df_2019.columns = [col.lower().replace(" ", "_") for col in df_2019.columns]

    print("Column names standardized.")

    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

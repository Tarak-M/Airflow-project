import pandas as pd

def convert_data_types(**kwargs):
    ti = kwargs['ti']
    df_2018_json = ti.xcom_pull(task_ids='standardize_columns', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='standardize_columns', key='df_2019_clean')

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    for df in [df_2018, df_2019]:
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)

    print("Data types converted.")

    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

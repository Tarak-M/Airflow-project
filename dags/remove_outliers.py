import pandas as pd
import numpy as np

def remove_outliers(**kwargs):
    ti = kwargs['ti']
    df_2018_json = ti.xcom_pull(task_ids='convert_data_types', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='convert_data_types', key='df_2019_clean')

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    for df in [df_2018, df_2019]:
        for col in df.select_dtypes(include=[np.number]).columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            df = df[(df[col] >= (q1 - 1.5 * iqr)) & (df[col] <= (q3 + 1.5 * iqr))]

    print("Outliers removed.")

    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

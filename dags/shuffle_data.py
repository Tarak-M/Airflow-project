import pandas as pd

def shuffle_data(**kwargs):
    ti = kwargs['ti']
   

    # Pull cleaned data from XCom
    df_2018_json = ti.xcom_pull(task_ids='remove_outliers', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='remove_outliers', key='df_2019_clean')

    df_2018 = pd.read_json(df_2018_json).sample(frac=1).reset_index(drop=True)
    df_2019 = pd.read_json(df_2019_json).sample(frac=1).reset_index(drop=True)

    print("Data shuffled.")

    ti.xcom_push(key='df_2018_clean', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_clean', value=df_2019.to_json())

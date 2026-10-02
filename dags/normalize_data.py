import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_data(**kwargs):
    ti = kwargs['ti']
    
    # Pull cleaned data from XCom
    df_2018_json = ti.xcom_pull(task_ids='remove_outliers', key='df_2018_clean')
    df_2019_json = ti.xcom_pull(task_ids='remove_outliers', key='df_2019_clean')

    if df_2018_json is None or df_2019_json is None:
        raise ValueError("No data received from remove_outliers task")

    df_2018 = pd.read_json(df_2018_json)
    df_2019 = pd.read_json(df_2019_json)

    scaler = MinMaxScaler()

    # Normalize only numeric columns
    numeric_columns_2018 = df_2018.select_dtypes(include=['float64', 'int64']).columns
    numeric_columns_2019 = df_2019.select_dtypes(include=['float64', 'int64']).columns

    df_2018[numeric_columns_2018] = scaler.fit_transform(df_2018[numeric_columns_2018])
    df_2019[numeric_columns_2019] = scaler.fit_transform(df_2019[numeric_columns_2019])

    print("Data normalized successfully.")

    # Push normalized data back to XCom
    ti.xcom_push(key='df_2018_normalized', value=df_2018.to_json())
    ti.xcom_push(key='df_2019_normalized', value=df_2019.to_json())

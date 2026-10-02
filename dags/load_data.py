import pandas as pd

def load_data(**kwargs):
    ti = kwargs['ti']  # Task Instance
    df_2018 = pd.read_csv("~/Input/medicare_data_2018.csv")
    df_2019 = pd.read_csv("~/Input/medicare_data_2019.csv")

    print("Data loaded successfully.")

    # Store data in XCom
    ti.xcom_push(key='df_2018', value=df_2018.to_json())  # Convert to JSON for XCom storage
    ti.xcom_push(key='df_2019', value=df_2019.to_json())

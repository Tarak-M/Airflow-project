from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
import os


# Define Paths (Ensure correct path inside Docker)
input_path_2018 = "~/Input/medicare_data_2018.csv"
input_path_2019 = "~/Input/medicare_data_2019.csv"
output_folder = "~/Output/"
parquet_output_path = os.path.join(output_folder, "cleaned_medicare_data.parquet")
csv_output_path = os.path.join(output_folder, "cleaned_medicare_data.csv")



default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 9, 10),
    "retries": 0,
    "retry_delay": timedelta(seconds=15),
}

dag = DAG(
    "healthcare_data_pipeline",
    default_args=default_args,
    schedule_interval=timedelta(1),
    catchup=False,
)

# Task 1: Check if files exist (BashOperator)
task_check_files = BashOperator(
    task_id="check_files",
    bash_command=f"test -f {input_path_2018} && test -f {input_path_2019}",
    dag=dag,
)

# Task 2: Load Data (PythonOperator)
from load_data import load_data
task_load_data = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

# Task 3-9: Data Transformations (Drop Duplicates, Handle Missing Values, etc.)
from drop_duplicates import drop_duplicates
task_drop_duplicates = PythonOperator(
    task_id="drop_duplicates",
    python_callable=drop_duplicates,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

from handle_missing_values import handle_missing_values
task_handle_missing_values = PythonOperator(
    task_id="handle_missing_values",
    python_callable=handle_missing_values,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

from standardize_columns import standardize_columns
task_standardize_columns = PythonOperator(
    task_id="standardize_columns",
    python_callable=standardize_columns,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

from convert_data_types import convert_data_types
task_convert_data_types = PythonOperator(
    task_id="convert_data_types",
    python_callable=convert_data_types,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

from remove_outliers import remove_outliers
task_remove_outliers = PythonOperator(
    task_id="remove_outliers",
    python_callable=remove_outliers,
    provide_context=True,  # Allow passing task context
    dag=dag,
)

from shuffle_data import shuffle_data
task_shuffle_data = PythonOperator(
    task_id="shuffle_data",
    python_callable=shuffle_data,
    provide_context=True,  # Allow passing task context
    dag=dag,
)


# Task : Save as CSV
from save_csv import save_csv
task_save_csv = PythonOperator(
    task_id="save_csv",
    python_callable=save_csv,
    provide_context=True,  # Allow passing task context
    dag=dag,
)


# Task : Send Email on Success
task_send_email = EmailOperator(
    task_id="send_email",
    to="taraksrinivasmallineni@gmail.com",
    subject="Healthcare Data Pipeline - Success",
    html_content="<h3>Data processing completed successfully!</h3>",
    dag=dag,
)

# Define Task Dependencies
(
    task_check_files
    >> task_load_data
    >> task_drop_duplicates
    >> task_handle_missing_values
    >> task_standardize_columns
    >> task_convert_data_types
    >> task_remove_outliers
    >> task_shuffle_data
    >> task_save_csv
    >> task_send_email
)

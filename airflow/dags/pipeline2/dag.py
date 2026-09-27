from airflow.models import DAG
from airflow.sdk import task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.timetables.trigger import CronTriggerTimetable
from pendulum import datetime, now, DateTime, from_format
from airflow.providers.google.cloud.operators.cloud_run import CloudRunExecuteJobOperator

# Create Simple DAG with Catch Up
with DAG( dag_id= 'pipeline2', 
          schedule= CronTriggerTimetable("0 0 * * *", timezone="Asia/Bangkok"),
          catchup= True,
          start_date= from_format('2026-01-01', 'YYYY-MM-DD', tz= 'Asia/Bangkok'),
          tags= ['csv->bq', 'p1'],
          max_active_runs= 1
        ) :
    
    # data_date
    @task(task_id= 'get_data_date')
    def get_data_date(data_interval_end : DateTime) : # Get `data_interval_end` 
        data_dt= data_interval_end.in_timezone('Asia/Bangkok')
        print(f'Run date is {now(tz= 'Asia/Bangkok').strftime("%Y-%m-%d %H:%M:%S")}')  # Use `data_interval_end` 
        print(f'Data date is {data_dt.strftime("%Y-%m-%d %H:%M:%S")}')  # Use `data_interval_end` 
        
    data_date= get_data_date()
    
    cloud_run_job = CloudRunExecuteJobOperator(
                                task_id='cloud_run_job',
                                project_id='PROJECT_ID',
                                region='REGION',
                                gcp_conn_id= 'GOOGLE_CLOUD_CONNECTION_ID',
                                job_name='JOB_NAME',
                                overrides={
                                            "container_overrides": [
                                                {
                                                    "env": [
                                                            {"name" : "NOTEBOOK_BUCKET",
                                                             "value" : "NOTEBOOK_BUCKET"},
                                                            {"name" : "NOTEBOOK_NAME",
                                                             "value" : "p2.ipynb"},
                                                            {"name": "RUN_DT", 
                                                             "value": "{{ data_interval_end.in_tz('Asia/Bangkok').strftime('%Y-%m-%d') }}"},
                                                            {"name": "GCS_PROJECT", 
                                                             "value": "GCS_PROJECT"},
                                                            {"name": "GCS_BUCKET", 
                                                             "value": "GCS_BUCKET"},
                                                            {"name": "GCS_FILE_PATH", 
                                                             "value": "GCS_FILE_PATH"},
                                                            {"name": "BQ_TARGET_PROJECT", 
                                                             "value": "BQ_TARGET_PROJECT"},
                                                            {"name": "BQ_TARGET_SCHEMA", 
                                                             "value": "BQ_TARGET_SCHEMA"},
                                                            {"name": "BQ_TARGET_TABLE", 
                                                             "value": "BQ_TARGET_TABLE"},
                                                            ],
                                                }
                                            ],
                                            "timeout": "3600s",
                                        },
                                deferrable=True,
                                )
    data_date >> cloud_run_job
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

#-------------------------------------------------------------------------------
# these args will get passed on to each operator
# you can override them on a per-task basis during operator initialization

default_args = {
    'owner': 'qingcloud',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['johuo@yunify.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

#-------------------------------------------------------------------------------
# dag

dag = DAG(
    'qingcloud_test',
    default_args=default_args,
    description='qingcloud_test',
    schedule_interval=timedelta(days=1))

#-------------------------------------------------------------------------------
# first operator

date_operator = BashOperator(
    task_id='date_task',
    bash_command='date;echo `date`:qingcloud_test testing!>>/tmp/dag_test.log',  
    dag=dag)

#-------------------------------------------------------------------------------
# second operator

sleep_operator = BashOperator(
    task_id='sleep_task',
    depends_on_past=False,
    bash_command='sleep 5',
    dag=dag)

#-------------------------------------------------------------------------------
# third operator

def print_hello():
    return 'Hello world!'

hello_operator = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag)

#-------------------------------------------------------------------------------
# dependencies

sleep_operator.set_upstream(date_operator)
hello_operator.set_upstream(date_operator)


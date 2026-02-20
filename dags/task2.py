from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

with DAG(
    dag_id="task_2",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:
    task2 = KubernetesPodOperator(
        task_id="task2",
        name="task2-pod",
        namespace="development",
        image="python:3.10-slim",
        cmds=["echo", "completed task 2 successfully"],
        get_logs=True,
    )

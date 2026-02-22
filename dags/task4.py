from __future__ import annotations
import os
import pendulum

from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

NAMESPACE = os.getenv("AIRFLOW_POD_NAMESPACE", "development")

with DAG(
    dag_id="task_4",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:
    task4 = KubernetesPodOperator(
        task_id="task4",
        name="task4-pod",
        namespace=NAMESPACE,
        image="us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest",
        image_pull_policy="IfNotPresent",
        cmds=["echo", "completed task 2 successfully"],
        get_logs=True,
    )

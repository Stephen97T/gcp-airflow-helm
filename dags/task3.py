from __future__ import annotations

import pendulum
import os
from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.models.baseoperator import chain  # type: ignore[import-not-found]

NAMESPACE = os.getenv("RUN_TARGET_NAMESPACE", "development")

with DAG(
    dag_id="task_3",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:

    def create_task(step: int) -> KubernetesPodOperator:
        return KubernetesPodOperator(
            task_id=f"task{step}",
            name=f"task{step}-pod",
            namespace=NAMESPACE,
            image="python:3.10-slim",
            cmds=["echo", f"completed task {step} successfully"],
            get_logs=True,
        )

    steps = [1, 2, 3, 4, 5]

    tasks = [create_task(step) for step in steps]

    chain(*tasks)

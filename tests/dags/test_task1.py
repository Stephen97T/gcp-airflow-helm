import importlib
import sys
from tests.dags.airflow_mocks import install_fake_airflow


def test_task1_dag_and_task_definition()->None:
    """Import dags.task1 with Airflow mocked and validate calls to DAG and KubernetesPodOperator."""
    with install_fake_airflow() as fakes:
        fake_dag_cls = fakes["DAG"]
        fake_k8s_cls = fakes["KubernetesPodOperator"]

        # Import the DAG module; this should construct a DAG and one KubernetesPodOperator
        # Use reload in case it was already imported by another test
        if "dags.task1" in sys.modules:
            mod = importlib.reload(sys.modules["dags.task1"])
        else:
            mod = importlib.import_module("dags.task1")
        assert mod is not None

        # DAG should have been instantiated once with dag_id="task_1"
        assert fake_dag_cls.call_count == 1
        dag_call = fake_dag_cls.call_args
        assert dag_call.kwargs.get("dag_id") == "task_1"
        assert dag_call.kwargs.get("catchup") is False
        assert dag_call.kwargs.get("schedule") is None

        # KubernetesPodOperator should have been instantiated once with correct args
        assert fake_k8s_cls.call_count == 1
        task_call = fake_k8s_cls.call_args
        assert task_call.kwargs.get("task_id") == "task1"
        assert task_call.kwargs.get("name") == "task1-pod"
        assert task_call.kwargs.get("namespace") == "development"
        assert task_call.kwargs.get("image") == "python:3.10-slim"
        assert task_call.kwargs.get("cmds") == ["echo", "completed task 1 successfully"]
        assert task_call.kwargs.get("get_logs") is True

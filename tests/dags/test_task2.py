import importlib
import sys
from tests.dags.airflow_mocks import install_fake_airflow


def test_task2_kubernetes_pod_definition()->None:
    with install_fake_airflow() as fakes:
        fake_k8s_cls = fakes["KubernetesPodOperator"]

        if "dags.task2" in sys.modules:
            mod = importlib.reload(sys.modules["dags.task2"])
        else:
            mod = importlib.import_module("dags.task2")
        assert mod is not None

        # One KubernetesPodOperator should be created with the expected kwargs
        assert fake_k8s_cls.call_count == 1
        call = fake_k8s_cls.call_args
        kwargs = call.kwargs
        assert kwargs.get("task_id") == "task2"
        assert kwargs.get("name") == "task2-pod"
        assert kwargs.get("namespace") == "development"
        assert kwargs.get("image") == "python:3.10-slim"
        assert kwargs.get("cmds") == ["echo", "completed task 2 successfully"]
        assert kwargs.get("get_logs") is True

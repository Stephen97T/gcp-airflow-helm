import importlib
import sys
from tests.dags.airflow_mocks import install_fake_airflow


def test_task3_creates_five_kubernetes_tasks_and_chains_them()->None:
    with install_fake_airflow() as fakes:
        fake_k8s_cls = fakes["KubernetesPodOperator"]
        fake_chain = fakes["chain"]

        if "dags.task3" in sys.modules:
            mod = importlib.reload(sys.modules["dags.task3"])
        else:
            mod = importlib.import_module("dags.task3")
        assert mod is not None

        # We expect 5 tasks created (task1..task5)
        assert fake_k8s_cls.call_count == 5

        created_task_ids = [call.kwargs.get("task_id") for call in fake_k8s_cls.call_args_list]
        assert created_task_ids == [f"task{i}" for i in range(1, 6)]

        # Verify they all share the same base image/namespace pattern
        for call in fake_k8s_cls.call_args_list:
            kwargs = call.kwargs
            assert kwargs.get("namespace") == "development"
            assert kwargs.get("image") == "python:3.10-slim"
            assert kwargs.get("get_logs") is True

        # chain should have been called once with all created task objects
        assert fake_chain.call_count == 1
        # We don't assert exact objects here, just that it was invoked

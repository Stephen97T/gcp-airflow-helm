import importlib
import sys
from tests.dags.airflow_mocks import install_fake_airflow


def test_task4_kubernetes_pod_definition_uses_artifact_registry_image()->None:
    with install_fake_airflow() as fakes:
        fake_k8s_cls = fakes["KubernetesPodOperator"]

        if "dags.task4" in sys.modules:
            mod = importlib.reload(sys.modules["dags.task4"])
        else:
            mod = importlib.import_module("dags.task4")
        assert mod is not None

        # One KubernetesPodOperator should be created with the expected Artifact Registry image
        assert fake_k8s_cls.call_count == 1
        call = fake_k8s_cls.call_args
        kwargs = call.kwargs
        assert kwargs.get("task_id") == "task4"
        assert kwargs.get("name") == "task4-pod"
        assert kwargs.get("namespace") == "development"
        assert kwargs.get("image") == "us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest"
        assert kwargs.get("image_pull_policy") == "IfNotPresent"
        assert kwargs.get("cmds") == ["echo", "completed task 2 successfully"]
        assert kwargs.get("get_logs") is True

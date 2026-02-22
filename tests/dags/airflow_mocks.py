import types
from typing import Iterator, Any
from unittest.mock import MagicMock, patch
from contextlib import contextmanager


@contextmanager
def install_fake_airflow() -> Iterator[dict[str, Any]]:
    """Context manager that installs a fake airflow package tree into sys.modules.

    This uses patch.dict ensures that sys.modules is restored after the test.

    Yields:
        dict: A dictionary of the mock objects injected (DAG, BashOperator, etc.)
    """
    # Root package
    airflow_module = types.ModuleType("airflow")

    # Subpackages / modules we reference in DAGs
    models_module = types.ModuleType("airflow.models")
    dag_module = types.ModuleType("airflow.models.dag")
    operators_module = types.ModuleType("airflow.operators")
    bash_module = types.ModuleType("airflow.operators.bash")
    providers_module = types.ModuleType("airflow.providers")
    cncf_module = types.ModuleType("airflow.providers.cncf")
    kubernetes_module = types.ModuleType("airflow.providers.cncf.kubernetes")
    k8s_ops_module = types.ModuleType(
        "airflow.providers.cncf.kubernetes.operators.pod"
    )
    baseoperator_module = types.ModuleType("airflow.models.baseoperator")

    # Minimal fake classes / functions used in DAGs
    FakeDAG = MagicMock(name="DAG")
    FakeBashOperator = MagicMock(name="BashOperator")
    FakeKubernetesPodOperator = MagicMock(name="KubernetesPodOperator")
    fake_chain = MagicMock(name="chain")

    dag_module.DAG = FakeDAG  # type: ignore[attr-defined]
    bash_module.BashOperator = FakeBashOperator  # type: ignore[attr-defined]
    k8s_ops_module.KubernetesPodOperator = FakeKubernetesPodOperator  # type: ignore[attr-defined]
    baseoperator_module.chain = fake_chain  # type: ignore[attr-defined]

    # Wire package tree
    airflow_module.models = models_module  # type: ignore[attr-defined]
    airflow_module.operators = operators_module  # type: ignore[attr-defined]
    airflow_module.providers = providers_module  # type: ignore[attr-defined]
    models_module.dag = dag_module  # type: ignore[attr-defined]

    # Create a dictionary for patch.dict(sys.modules, ...)
    new_modules = {
        "airflow": airflow_module,
        "airflow.models": models_module,
        "airflow.models.dag": dag_module,
        "airflow.operators": operators_module,
        "airflow.operators.bash": bash_module,
        "airflow.providers": providers_module,
        "airflow.providers.cncf": cncf_module,
        "airflow.providers.cncf.kubernetes": kubernetes_module,
        "airflow.providers.cncf.kubernetes.operators.pod": k8s_ops_module,
        "airflow.models.baseoperator": baseoperator_module,
    }

    # Also fake pendulum, since DAGs import it
    pendulum_module = types.ModuleType("pendulum")
    pendulum_module.datetime = MagicMock(name="datetime")  # type: ignore[attr-defined]
    new_modules["pendulum"] = pendulum_module

    # Prepare the mocks dictionary to yield
    mocks = {
        "DAG": FakeDAG,
        "BashOperator": FakeBashOperator,
        "KubernetesPodOperator": FakeKubernetesPodOperator,
        "chain": fake_chain,
    }

    with patch.dict("sys.modules", new_modules):
        yield mocks


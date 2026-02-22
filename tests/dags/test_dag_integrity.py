import importlib
from tests.dags.airflow_mocks import install_fake_airflow


# NOTE: These tests are designed to run without a real Airflow installation.
# We fully mock the minimal Airflow API surface that our DAGs touch and then
# simply import the DAG modules. Any syntax/import errors in the DAG files
# will surface as test failures.


def test_import_all_dags_with_mocked_airflow()->None:
    """Ensure all DAG modules can be imported when Airflow is fully mocked.

    This is a pure unit test: it doesn't require a real Airflow install or DB.
    It just verifies that our DAG files are syntactically valid and that they
    can be imported successfully given the Airflow API surface we use.
    """
    with install_fake_airflow() as fakes:

        # Import each DAG module; any import error will fail the test.
        task1 = importlib.import_module("dags.task1")
        task2 = importlib.import_module("dags.task2")
        task3 = importlib.import_module("dags.task3")
        task4 = importlib.import_module("dags.task4")

        # Optional: basic sanity checks that our fake constructors were used.
        # We don't assert exact call counts here to keep the test robust to
        # small refactors, but we do check they were invoked at least once.
        assert fakes["DAG"].call_count >= 1
        assert fakes["KubernetesPodOperator"].call_count >= 1

        # Ensure modules imported and expose something (e.g., a `dag` attribute
        # in the context-managed style), but we don't depend on exact structure.
        assert task1 is not None
        assert task2 is not None
        assert task3 is not None
        assert task4 is not None

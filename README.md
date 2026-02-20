# GCP Airflow Helm

A robust, production-ready Airflow setup capable of running locally on **Minikube** and deploying to **Google Kubernetes Engine (GKE) Autopilot**. This project uses the official Apache Airflow Helm chart, customized for cost-efficiency and ease of use.

## 🚀 Architecture

*   **Orchestrator:** Apache Airflow 2.8+
*   **Executor:** `KubernetesExecutor` (Each task runs in its own isolated Pod)
*   **Database:** In-Cluster PostgreSQL (via Bitnami Helm chart) - *Keeps costs low for testing/free-tier*
*   **DAG Deployment:** Git-Sync (Sidecar container pulls DAGs directly from this repo)
*   **Infrastructure:**
    *   **Local:** Minikube
    *   **Production:** GKE Autopilot

## 🛠️ Prerequisites

Ensure you have the following installed (Windows/PowerShell recommended):

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/)
*   [Kubectl](https://kubernetes.io/docs/tasks/tools/)
*   [Helm](https://helm.sh/docs/intro/install/)
*   [GCloud SDK](https://cloud.google.com/sdk/docs/install) (for GKE deployment)

## 🏃 Quick Start: Local Development (Minikube)

1.  **Start Minikube:**
    ```powershell
    minikube start --cpus 4 --memory 8192
    ```

2.  **Add Airflow Helm Repository:**
    ```powershell
    helm repo add apache-airflow https://airflow.apache.org
    helm repo update
    ```

3.  **Install/Upgrade Airflow:**
    Run this command from the project root:
    ```powershell
    helm upgrade --install airflow apache-airflow/airflow -n airflow --create-namespace -f helm/values-local.yaml --debug
    ```

4.  **Access the Airflow UI:**
    Port-forward the webserver service to your localhost:
    ```powershell
    kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
    ```
    Open [http://localhost:8080](http://localhost:8080).
    *   **User:** `admin`
    *   **Password:** `admin`

## ☁️ Production: Google Kubernetes Engine (GKE)

1.  **Configure GKE Cluster:**
    Ensure you have a GKE Autopilot cluster running and `kubectl` is authenticated to it.

2.  **Deploy:**
    Use the production values file which is tuned for GKE:
    ```powershell
    helm upgrade --install airflow apache-airflow/airflow -n airflow --create-namespace -f helm/values-prod.yaml
    ```

## 🔄 DAG Development Workflow

This setup uses **Git-Sync**. You do not need to rebuild Docker images to update your DAGs.

1.  **Write DAGs:** Create Python files in the `dags/` folder (e.g., `dags/task1.py`).
2.  **Push to Git:** Commit and push your changes to your GitHub repository.
    ```bash
    git add .
    git commit -m "Add new DAG"
    git push origin main
    ```
3.  **Sync:** The Airflow Scheduler and Webserver pods have a sidecar that polls your repo every 60 seconds (configured in `values-local.yaml`).

**Important:** Update the `gitSync.repo` URL in your `helm/values-local.yaml` and `helm/values-prod.yaml` to match *your* repository URL.

## 📂 Project Structure

```
gcp-airflow-helm/
├── dags/                   # Python DAG files
│   └── task1.py            # Example DAG
├── helm/                   # Helm Configuration
│   ├── values-local.yaml   # Config for Minikube
│   └── values-prod.yaml    # Config for GKE
├── .claude/                # AI-generated documentation & guides
└── README.md               # This file
```

# ⚠️ Backup Before Upgrading Airflow!

**Before upgrading Airflow, always back up your PostgreSQL database!**

1. Ensure the `data` directory exists:
   ```powershell
   if (!(Test-Path -Path "data")) { New-Item -ItemType Directory -Path "data" }
   ```
2. Backup your database:
   ```powershell
   kubectl exec -it airflow-postgresql-0 -n airflow -- pg_dump -U postgres postgres > data/airflow_backup_$(Get-Date -Format "yyyyMMdd").sql
   ```

---

# Helm Chart Configuration for Apache Airflow

This folder contains all configuration files for deploying Apache Airflow using Helm on Kubernetes (Minikube or GKE).

## 📁 File Overview

| File                        | Purpose                                                      |
|-----------------------------|--------------------------------------------------------------|
| `values-local.yaml`         | Local (Minikube) deployment configuration                    |
| `values-prod.yaml`          | Production (GKE) deployment configuration                    |
| `values-local-upgrade.yaml` | For testing upgrades (e.g., Airflow 3.x) locally             |
| `secrets-template.yaml`     | Template for secrets (copy and fill to create `secrets.yaml`) |
| `secrets.yaml`              | Actual secrets (required for deployment, not committed)       |
| `default-values-reference.yaml` | Reference: full default values from upstream chart         |

## 🛡️ Secrets Setup

1. Copy `secrets-template.yaml` to `secrets.yaml`:
   ```powershell
   cp helm/secrets-template.yaml helm/secrets.yaml
   ```
2. Edit `secrets.yaml` and fill in strong values for all fields (especially passwords and keys).

## 🚀 Step-by-Step Deployment

### Prerequisites
- Kubernetes cluster (Minikube or GKE)
- Helm installed
- Namespace created (e.g., `airflow`)

### 1. Start Minikube (if local)
```powershell
minikube start --driver=docker --cpus 4 --memory 6144
```

### 2. Create Namespace
```powershell
kubectl create namespace airflow
```

### 3. Deploy Airflow

#### Local (Minikube):
```powershell
helm install airflow apache-airflow/airflow --version 1.12.0 -f helm/values-local.yaml -f helm/secrets.yaml -n airflow
```

#### Production (GKE):
```powershell
helm install airflow apache-airflow/airflow --version 1.12.0 -f helm/values-prod.yaml -f helm/secrets.yaml -n airflow
```

### 4. Access Airflow UI

**Minikube:**
```powershell
kubectl port-forward svc/airflow-webserver 8081:8080 -n airflow
kubectl exec -it deploy/airflow-scheduler -n airflow -- airflow users create --username admin --firstname Name --lastname User --role Admin --email name@example.com --password password
# Open http://localhost:8080
```

**GKE:**
```powershell
kubectl get svc -n airflow airflow-webserver
# Open http://<EXTERNAL-IP>:8080
```

## 🔄 Upgrading Airflow

- To test upgrades locally, use `values-local-upgrade.yaml` and set the desired Airflow version.
- Always back up your database before upgrading!
- Update the `images.airflow.tag` or `defaultAirflowTag` in your values file.
- Check helm version compatibility with the Airflow version you want to upgrade to: *helm search repo apache-airflow/airflow --versions*
- Upgrade with:
  ```powershell
  helm upgrade airflow apache-airflow/airflow --version 1.18.0 -f helm/values-local-upgrade.yaml -f helm/secrets.yaml -n airflow
  ```

## 📝 Updating Configuration

1. Edit the relevant `values-*.yaml` file.
2. Apply changes:
   ```powershell
   helm upgrade airflow apache-airflow/airflow -f helm/values-local.yaml -f helm/secrets.yaml -n airflow
   # or for prod:
   helm upgrade airflow apache-airflow/airflow -f helm/values-prod.yaml -f helm/secrets.yaml -n airflow
   ```

## 🛠️ Troubleshooting & Tips

- **Check Helm release history:**
  ```powershell
  helm history airflow -n airflow
  ```
- **Rollback to previous version:**
  ```powershell
  helm rollback airflow <REVISION> -n airflow
  ```
- **Check if service account can create pods:**
  ```powershell
  kubectl auth can-i create pods -n airflow --as system:serviceaccount:airflow:airflow-scheduler
  ```
- **Check logs:**
  ```powershell
  kubectl logs <pod-name> -n airflow
  ```

## 🗑️ Uninstall
Whenever you want to uninstall Airflow, run:
```powershell
helm uninstall airflow -n airflow
kubectl delete pods --all -n airflow
kubectl delete pvc --all -n airflow # Deletes postgresql data, so be cautious!
kubectl delete namespace airflow
```

In case you are experiencing a lot of bugs with installing airflow, you can reset with these commands and try installing again using helm.

---

For more details, see the [official Apache Airflow Helm Chart documentation](https://airflow.apache.org/docs/helm-chart/stable/index.html).

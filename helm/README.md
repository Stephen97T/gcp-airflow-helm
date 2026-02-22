# Helm Configuration

This folder contains Helm chart configuration for Apache Airflow deployment.

## 📁 Files

- **`values-prod.yaml`** - Main configuration file for Airflow Helm chart GKE
- **`values-local.yaml`** - Configuration file optimized for local Minikube deployment
- **`default-values-reference.yaml`** - Complete default values from official chart (reference only)

### Security Notes:

**For production:** Consider using:
- Google Secret Manager

## 🚀 Deploying Airflow

### Prerequisites:

1. Kubernetes cluster running (Minikube or GKE)
2. `airflow` namespace exists

### Start minikube (if using Minikube):

```powershell
minikube start --driver=docker --cpus 4 --memory 6144 # can adjust to memory available on your machine
```

### Create Namespace:

```powershell
kubectl create namespace airflow
```

### Deploy Command:

#### Local Minikube:
Need to use specific helm version for compatibility with airflow 2.8.1.
see ***helm search repo apache-airflow/airflow --versions***
```powershell
# Deploy to local Minikube cluster
helm install airflow apache-airflow/airflow --version 1.12.0 -f helm/values-local.yaml -n airflow
```

#### GKE:
```powershell
# Deploy to current cluster
 helm install airflow apache-airflow/airflow --version 1.12.0 -f helm/values-prod.yaml -n airflow
```

### Access Airflow UI:

**For Minikube:**
```powershell
# Port forward to localhost
kubectl port-forward svc/airflow-webserver 8081:8080 -n airflow # Port 8080 was not available, using 8081 instead

kubectl exec -it deploy/airflow-scheduler -n airflow -- airflow users create --username admin --firstname Stephen --lastname User --role Admin --email stephen@example.com --password admin


# Open browser to: http://localhost:8080
```

**For GKE:**
```powershell
# Get LoadBalancer external IP
kubectl get svc -n airflow airflow-webserver

# Open browser to: http://<EXTERNAL-IP>:8080
```

**Login credentials:**
- Username
- Password

## 🔧 Configuration Highlights

### Executor
- **KubernetesExecutor** - Each task runs in its own pod (Autopilot-friendly)

### Database
- **In-cluster PostgreSQL** - 5Gi storage (free tier optimized)

### DAGs
- **Git-Sync enabled** - Automatically pulls DAGs from GitHub
- Update the repo URL in `values.yaml` before deploying

### Resources
- Optimized for GKE Autopilot constraints
- Scheduler: 500m CPU, 1Gi RAM
- Webserver: 500m CPU, 1Gi RAM

## 📝 Updating Configuration

1. Edit `values.yaml`
2. Apply changes:
   ```powershell
   helm upgrade airflow apache-airflow/airflow `
     --namespace airflow `
     --values helm/values.yaml
   ```

## 🔄 Rollback

If something goes wrong:
```powershell
# View release history
helm history airflow -n airflow

# Rollback to previous version (e.g. revision 1)
# helm rollback <release-name> <revision-number> -n <namespace>
helm rollback airflow 1 -n airflow
```

## 🗑️ Uninstall

```powershell
# Remove Airflow deployment (keeps secrets)
helm uninstall airflow -n airflow

# Optional: Delete namespace and all resources
kubectl delete namespace airflow
```

## 📚 More Information

See `.claude/helm-configuration.md` for detailed configuration documentation.

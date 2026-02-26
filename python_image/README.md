# Python Image: Build & Usage Guide

This guide explains how to build and use the Docker image for the `python_image` (e.g., for task4), both locally (Minikube) and for Google Artifact Registry (GCP).

---

## 🐳 Build Locally for Minikube

First, configure your shell to use the Minikube Docker daemon:

```powershell
minikube docker-env --shell powershell | Invoke-Expression
```

Test if Docker is using the Minikube context:

```powershell
docker info | Select-String Name
```

Build the image from the project root:

```powershell
docker compose -f python_image/docker-compose.yml build
```

---

## 🏷️ Tag & Push to Google Artifact Registry (GCP)

1. **Tag the image for GCP Artifact Registry:**

   Replace `<PROJECT_ID>` with your GCP project ID if needed.

   ```powershell
   docker tag python_image_task4:latest us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest
   ```

2. **Authenticate Docker with GCP:**

   ```powershell
gcloud auth configure-docker us-east1-docker.pkg.dev
   ```

3. **Push the image:**

   ```powershell
   docker push us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest
   ```

---

## 📝 Notes
- Always run Docker commands from the project root for correct context.
- The image name in Artifact Registry is: `us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest`
- Update your Kubernetes/Helm manifests to use this image when deploying to GKE.

---

## Example: Build, Tag, and Push (All Steps)

```powershell
minikube docker-env --shell powershell | Invoke-Expression
# Build image for local testing
cd C:\Users\Stephen\PycharmProjects\gcp-airflow-helm

docker compose -f python_image/docker-compose.yml build
# Tag for GCP

docker tag python_image_task4:latest us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest
# Authenticate and push

gcloud auth configure-docker us-east1-docker.pkg.dev
docker push us-east1-docker.pkg.dev/gcp-airflow-helm/tasks-repo/task4:latest
```

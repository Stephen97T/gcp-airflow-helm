# Kubernetes Namespace Management

This directory contains the configuration for initializing the `development` and `production` namespaces with the correct permissions for Airflow.
To add more namespaces just copy one of the folders (e.g. development or production) and rename the namespace in the ***values.yaml***

## Structure

*   `charts/`: The base Helm chart that creates a Namespace, Role, and RoleBinding.
*   `development/values.yaml`: Configuration specific to the development environment.
*   `production/values.yaml`: Configuration specific to the production environment.

## How to Apply (Trigger with Helm)

To create the **Development** namespace and permissions:

```bash
helm upgrade --install airflow-dev-ns namespaces/charts -f namespaces/development/values.yaml
```

To create the **Production** namespace and permissions:

```bash
helm upgrade --install airflow-prod-ns namespaces/charts -f namespaces/production/values.yaml
```

## Verification

After running the commands, you can verify the permissions are set correctly:

```bash
# Check if the RoleBinding exists in development
kubectl get rolebinding airflow-worker-cross-namespace -n development

# Check if the RoleBinding exists in production
kubectl get rolebinding airflow-worker-cross-namespace -n production
```

## Debugging Namespace Permissions

If Airflow pods fail to start due to RBAC issues, check permissions with:

```powershell
kubectl auth can-i create pods -n development --as system:serviceaccount:airflow:airflow-worker
```

This command verifies if the Airflow worker service account can create pods in the development namespace.

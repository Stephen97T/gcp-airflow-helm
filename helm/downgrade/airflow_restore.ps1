# ===================================================================
# Airflow 2 Database Restore & Helm Downgrade Script (PowerShell)
# ===================================================================
# WARNING: This script will DROP the airflow_db database.
# Make sure you have backups before running.
# ===================================================================

$Namespace = "airflow"
$PostgresPod = "airflow-postgresql-0"
$PostgresUser = "postgres"
$PostgresPassword = "postgres" # Update with actual password
$DbName = "airflow_db"
$BackupFileLocal = "data/airflow_backup_20260227.sql"
$BackupFilePod = "/tmp/airflow_backup.sql"
$BackupFileUtf8 = "/tmp/airflow_utf8.sql"

Write-Host "==> 1. Pause Airflow pods to prevent DB connections..."
$PodsToScale = @(
    "airflow-api-server",
    "airflow-dag-processor",
    "airflow-scheduler",
    "airflow-webserver",
    "airflow-statsd",
    "airflow-worker"
)
foreach ($pod in $PodsToScale) {
    kubectl scale deployment $pod --replicas=0 -n $Namespace
}
kubectl scale statefulset airflow-triggerer --replicas=0 -n airflow
kubectl delete job airflow-run-airflow-migrations -n airflow

Write-Host "==> 2. Disable new connections..."
kubectl exec -n $Namespace $PostgresPod -- bash -c "PGPASSWORD='$PostgresPassword' psql -U $PostgresUser -d postgres -c 'ALTER DATABASE $DbName WITH ALLOW_CONNECTIONS false;'"
Write-Host "==> 3. Kill active connections..."

kubectl exec -n $Namespace $PostgresPod -- `
env PGPASSWORD=$PostgresPassword `
psql -U $PostgresUser -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$DbName' AND pid <> pg_backend_pid();"

Start-Sleep -Seconds 3

Write-Host "==> 4. Drop and recreate DB..."

kubectl exec -n $Namespace $PostgresPod -- `
env PGPASSWORD=$PostgresPassword `
psql -U $PostgresUser -d postgres -c "DROP DATABASE IF EXISTS $DbName;"

Start-Sleep -Seconds 5
kubectl exec -n $Namespace -it $PostgresPod -- bash -c "PGPASSWORD='$PostgresPassword' psql -U $PostgresUser -d postgres -c 'CREATE DATABASE $DbName;'"

Write-Host "==> 5. Copy backup file to PostgreSQL pod..."
kubectl cp $BackupFileLocal "${PostgresPod}:$BackupFilePod" -n $Namespace

Write-Host "==> 6. Convert backup to UTF-8 encoding..."
kubectl exec -n $Namespace -it $PostgresPod -- bash -c "iconv -f UTF-16 -t UTF-8 $BackupFilePod > $BackupFileUtf8"

Write-Host "==> 7. Restore the database from backup..."
kubectl exec -n $Namespace -it $PostgresPod -- bash -c "PGPASSWORD='$PostgresPassword' psql -U $PostgresUser -d $DbName -f $BackupFileUtf8"

Write-Host "==> 8. Verify Alembic version..."
kubectl exec -n $Namespace $PostgresPod -- `
env PGPASSWORD=$PostgresPassword `
psql -U $PostgresUser -d $DbName -c "SELECT * FROM alembic_version;"

Write-Host "==> 9. Rollback 1 version before via Helm..."
$lastRev = (helm history airflow -n airflow --max 2 | Select-Object -Skip 1 | ForEach-Object { $_.Split(" ")[0] })[0]
helm rollback airflow $lastRev -n airflow

#helm upgrade airflow apache-airflow/airflow --version 1.12.0 -f helm/values-local.yaml -f helm/secrets.yaml -n $Namespace

Write-Host "==> 10. Clean up Airflow 3 deployments..."
kubectl delete pod airflow-triggerer-0  -n $Namespace
kubectl delete deployment airflow-api-server -n $Namespace
kubectl delete deployment airflow-dag-processor -n $Namespace

Write-Host "==> Restore complete! Check pod statuses with: kubectl get pods -n $Namespace"
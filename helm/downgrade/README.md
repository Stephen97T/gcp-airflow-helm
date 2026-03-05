# Airflow Database Restore & Helm Downgrade Guide

This guide explains how to use the `airflow_restore.ps1` PowerShell script to restore your Airflow metadata database from a backup and downgrade your Airflow deployment using Helm. **Read all steps and warnings before running the script!**

---

## ⚠️ Warnings
- This script will **DROP** your Airflow metadata database (`airflow_db`). All existing data will be lost and replaced by the backup.
- Make sure you have a valid backup file before proceeding.
- This process will cause downtime for your Airflow deployment.
- Ensure you update the script variables for your environment (namespace, pod, passwords, etc).

---

## 📝 Prerequisites
- You have a working Kubernetes cluster with Airflow deployed via Helm.
- You have a backup SQL file (e.g., `data/airflow_backup_20260227.sql`).
- You have `kubectl`, `helm`, and PowerShell available on your system.

---

## 🚀 Steps Performed by the Script

1. **Pause Airflow Pods**
   - Scales down all Airflow deployments/statefulsets to 0 replicas to prevent new DB connections.
2. **Disable New DB Connections**
   - Disables new connections to the Airflow metadata database using PostgreSQL commands.
3. **Terminate Existing DB Sessions**
   - Kills all active sessions to the Airflow metadata database.
4. **Drop and Recreate the Database**
   - Drops the `airflow_db` database and recreates it empty.
5. **Copy Backup File to Pod**
   - Copies your local backup SQL file into the PostgreSQL pod.
6. **Convert Backup to UTF-8**
   - Converts the backup file encoding to UTF-8 (if needed; adjust encoding if your backup is not UTF-16).
7. **Restore the Database**
   - Restores the database from the backup file inside the pod.
8. **Verify Alembic Version**
   - Checks the Alembic migration version in the restored database.
9. **Downgrade Airflow via Helm**
   - Runs a Helm upgrade to deploy the desired Airflow version (e.g., 2.8.2).
10. **Clean Up Old Deployments**
    - Deletes Airflow 3.x deployments that are not present in 2.x.

---

## 🛠️ How to Use

1. **Edit the script if needed:**
   - Set the correct namespace, pod name, database name, passwords, and backup file paths at the top of `airflow_restore.ps1`.
2. **Run the script in PowerShell:**
   ```powershell
   .\helm\downgrade\airflow_restore.ps1
   ```
3. **Monitor progress:**
   - The script will print each step. Watch for errors.
4. **Check pod status:**
   - After completion, run:
     ```powershell
     kubectl get pods -n airflow
     ```

---

## 🧩 Troubleshooting
- If you see errors about database connections, make sure all Airflow pods are scaled down.
- If the restore fails, check the encoding of your backup file and adjust the `iconv` command in the script if needed.
- If you see Alembic migration errors after restore, you may need to run `airflow db stamp heads` inside the scheduler pod.
- Ensure the PostgreSQL password and user match your deployment; update `$PostgresPassword` and `$PostgresUser` in the script as needed.

---

## 📚 More Info
- See the main project README for backup/restore best practices and upgrade/downgrade tips.
- Always test restores in a non-production environment first!
- For Linux/macOS, use the bash version of the script if needed.

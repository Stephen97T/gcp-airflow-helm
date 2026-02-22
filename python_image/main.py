import os
from google.cloud import storage # type: ignore


def write_local_file(file_name: str, content: str) -> None:
    """Writes a file to the local data directory."""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"File '{file_name}' written to '{data_dir}'.")

def write_to_gcs(file_name: str, content: str) -> None:
    """Uploads a file to a GCS bucket."""
    bucket_name = os.environ.get("GCP_BUCKET")
    if not bucket_name:
        raise ValueError("GCP_BUCKET environment variable not set.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content)
    print(f"File '{file_name}' uploaded to bucket '{bucket_name}'.")

def main() -> None:
    """
    Writes a dummy file to a GCS bucket or a local directory.
    """
    environment = os.environ.get("ENVIRONMENT", "local")
    dummy_content = "This is a dummy file."
    file_name = "dummy_file.txt"

    if environment == "local":
        write_local_file(file_name, dummy_content)
    else:
        write_to_gcs(file_name, dummy_content)

if __name__ == "__main__":
    main()

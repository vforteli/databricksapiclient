import os
import glob
import base64
import requests
from typing import Union


def get_required_env(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise KeyError(f"Forgot '{key} in env?")

    return value


def mkdirs(path: str) -> requests.Response:
    payload = {"path": path}

    return requests.post(
        f"{DATABRICKS_BASE_URL}/api/2.0/workspace/mkdirs", json=payload, headers=HEADERS)


def import_file(databricks_path: str, local_path: str) -> requests.Response:
    """
    Import file from local path to databricks path
    Defaults to overwriting and format AUTO
    """

    with open(local_path, "rb") as file:
        content_encoded = base64.b64encode(file.read()).decode("utf-8")

    payload: dict[str, Union[str, bool]] = {
        "format": "AUTO",
        "path": databricks_path,
        "language": "PYTHON",
        "content": content_encoded,
        "overwrite": True
    }

    return requests.post(
        f"{DATABRICKS_BASE_URL}/api/2.0/workspace/import", json=payload, headers=HEADERS)


def delete_path(databricks_path: str) -> requests.Response:
    """
    Recursively delete a path in databricks
    """

    payload: dict[str, Union[str, bool]] = {
        "path": databricks_path,
        "recursive": True
    }

    return requests.post(
        f"{DATABRICKS_BASE_URL}/api/2.0/workspace/delete", json=payload, headers=HEADERS)


def upload_directory(source_directory: str, destination_directory: str):
    """
    Recursively upload folder to databricks
    """

    # Keep track of already created directories so we dont try to create them repeatedly
    created_directories = set[str]()

    paths = (path for path in glob.glob(source_directory +
                                        '/**/*', recursive=True) if os.path.isfile(path))

    for path in paths:
        relative_path = os.path.relpath(path, source_directory)

        databricks_file_path = os.path.join(
            destination_directory, relative_path).replace("\\", "/")

        databricks_dir_path = os.path.dirname(databricks_file_path)

        if databricks_dir_path and databricks_dir_path not in created_directories:
            mkdirs(databricks_dir_path)
            created_directories.add(databricks_dir_path)

        result = import_file(databricks_file_path, path)
        print(f"File: {databricks_file_path}, status: {result.status_code}")


DATABRICKS_BASE_URL = get_required_env("DATABRICKS_BASE_URL")
DATABRICKS_TOKEN = get_required_env("DATABRICKS_TOKEN")
DATABRICKS_SOURCE_DIRECTORY = get_required_env("DATABRICKS_SOURCE_DIRECTORY")
DATABRICKS_DESTINATION_DIRECTORY = get_required_env(
    "DATABRICKS_DESTINATION_DIRECTORY")


HEADERS = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}


print(f"Deleting old files in path {DATABRICKS_DESTINATION_DIRECTORY}")
delete_path(DATABRICKS_DESTINATION_DIRECTORY)

print("Uploading stuff to Databricks...")
upload_directory(DATABRICKS_SOURCE_DIRECTORY, DATABRICKS_DESTINATION_DIRECTORY)

print("Done...")

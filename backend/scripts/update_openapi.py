import requests
import json
import time
import subprocess
import os
import sys


def fetch_openapi(
    url="http://localhost:8000/openapi.json", output_path="docs/openapi/openapi.json"
):
    print(f"Fetching OpenAPI spec from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        spec = response.json()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(spec, f, indent=2)
        print(f"Successfully saved OpenAPI spec to {output_path}")
        return True
    except Exception as e:
        print(f"Error fetching OpenAPI spec: {e}")
        return False


if __name__ == "__main__":
    # If a server is already running, just fetch it
    if fetch_openapi():
        sys.exit(0)

    # Otherwise, try to start the server briefly
    print("Server not found. Attempting to start server briefly...")
    uv_python = os.environ.get("UV_PYTHON", sys.executable)
    process = subprocess.Popen(
        [uv_python, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="backend"
    )

    # Wait for server to start
    max_retries = 10
    success = False
    for i in range(max_retries):
        time.sleep(1)
        if fetch_openapi():
            success = True
            break
        print(f"Retry {i + 1}/{max_retries}...")

    process.terminate()
    if success:
        sys.exit(0)
    else:
        print("Failed to fetch OpenAPI spec after server start attempt.")
        sys.exit(1)

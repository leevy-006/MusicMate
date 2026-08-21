import os
import requests
import time
import json
from typing import Dict, Any, Optional


class ACEStepRemoteClient:
    """
    Python client for the ACE-Step API.
    Encapsulates the complete asynchronous workflow: submitting a task, polling for results, and downloading audio.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the client.

        :param base_url: The base URL of the API server. Must be provided via argument or environment variable.
        :param api_key: Optional API key for authentication.
        """
        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            # Read from environment variable matching your .env file
            env_url = os.environ.get("ACE_STEP_URL")
            if env_url:
                self.base_url = env_url.rstrip("/")
            else:
                raise ValueError(
                    "Missing base_url. Please provide it in arguments or set the ACE_STEP_URL environment variable."
                )

        self.api_key = api_key or os.environ.get("ACE_STEP_API_KEY")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handles API responses, checking for HTTP and API-level errors."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP request failed: {e}, Response: {response.text}")

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from server: {response.text}")

        if isinstance(data, list):
            data = {"code": 200, "data": data}
        elif not isinstance(data, dict):
            raise Exception(f"Unexpected response format from server: {data}")

        if data.get("code", 200) != 200:
            error_msg = data.get("error", "Unknown API Error")
            raise Exception(f"API Error (Code {data.get('code')}): {error_msg}")

        return data

    @staticmethod
    def _extract_first_record(payload: Any) -> Optional[Dict[str, Any]]:
        """Normalize list-based payloads to a single dictionary entry when possible."""
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, list) and payload:
            first_item = payload[0]
            if isinstance(first_item, dict):
                return first_item
        return None

    def release_task(self, payload: Dict[str, Any]) -> str:
        """
        Submits a music generation task.

        :param payload: Dictionary containing generation parameters (e.g., lyrics, tags).
        :return: The task_id string.
        """
        url = f"{self.base_url}/release_task"
        print(f"[INFO] Submitting task to {url}...")

        response = self.session.post(url, json=payload)
        data = self._handle_response(response)

        task_id = data.get("task_id")
        if not task_id:
            data_payload = data.get("data")
            record = self._extract_first_record(data_payload)
            task_id = record.get("task_id") if record else None

        if not task_id:
            raise Exception(f"Task submission successful but no task_id found in response: {data}")

        print(f"[INFO] Task submitted successfully. Task ID: {task_id}")
        return task_id

    def query_result(self, task_id: str) -> Dict[str, Any]:
        """
        Queries the status of a specific task.

        :param task_id: The ID of the task to check.
        :return: The full result data dictionary.
        """
        url = f"{self.base_url}/query_result"
        payload = {"task_id_list": [task_id]}

        response = self.session.post(url, json=payload)
        result = self._handle_response(response)

        if isinstance(result.get("data"), list):
            record = self._extract_first_record(result.get("data"))
            if record:
                return record

        return result

    def generate_music(self, payload: Dict[str, Any], poll_interval: int = 5, timeout: int = 600) -> Dict[str, Any]:
        """
        High-level method to generate music and wait for completion.

        :param payload: Generation parameters.
        :param poll_interval: Seconds to wait between status checks.
        :param timeout: Maximum seconds to wait before giving up.
        :return: The final successful result data containing audio info.
        """
        task_id = self.release_task(payload)

        start_time = time.time()
        print(f"[INFO] Polling for results (Interval: {poll_interval}s, Timeout: {timeout}s)...")

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout} seconds.")

            result = self.query_result(task_id)

            if isinstance(result, list):
                record = self._extract_first_record(result)
                if record:
                    result = record

            status = None
            if isinstance(result, dict):
                status = result.get("status")
                data_payload = result.get("data")
                if status is None:
                    record = self._extract_first_record(data_payload)
                    if record:
                        status = record.get("status")
                if status is None and isinstance(data_payload, dict):
                    status = data_payload.get("status")

            if status == 1 or status == "success" or status == "completed":
                print("[INFO] Task completed successfully!")
                return result

            print(f"[INFO] Task status: {status}. Waiting {poll_interval}s...")
            time.sleep(poll_interval)
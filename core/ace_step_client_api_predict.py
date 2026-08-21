import requests
from config.settings import ACE_STEP_REMOTE_URL


class ACEStepRemoteClient:
    """HTTP client that communicates with the remote ACE-Step 1.5 server."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or ACE_STEP_REMOTE_URL

    def generate_music(self, lyrics: str, tags: str, duration: int = 120) -> dict:
        """
        Send a generation request to the remote ACE-Step server.

        Args:
            lyrics: Structured lyrics with section tags like [verse], [chorus].
            tags: Comma-separated style descriptors.
            duration: Target song duration in seconds.

        Returns:
            A dict with 'status' and either 'audio_url' or 'message'.
        """
        payload = {
            "data": [tags, lyrics, duration, False],
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/predict",
                json=payload,
                timeout=300,
            )
            response.raise_for_status()
            result = response.json()

            audio_url = result.get("data", [None])[0]
            return {"status": "success", "audio_url": audio_url}
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": f"Cannot connect to ACE-Step server at {self.base_url}. "
                           "Make sure it is running and accessible.",
            }
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "ACE-Step server timed out (300s)."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
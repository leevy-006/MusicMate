from langchain_core.tools import tool
from config.settings import ACE_STEP_REMOTE_URL
from core.ace_step_client import ACEStepRemoteClient

ace_client = ACEStepRemoteClient(base_url=ACE_STEP_REMOTE_URL)


@tool
def generate_music(lyrics: str, style_tags: str, duration: int = 120) -> str:
    """
    Call the remote ACE-Step 1.5 to generate music based on lyrics and style tags.

    Args:
        lyrics: Structured lyrics containing tags like [verse], [chorus], [bridge].
        style_tags: Comma-separated style descriptors (e.g., "pop, female vocal, 120 bpm").
        duration: Song duration in seconds (recommended 60-180).

    Returns:
        A string containing the generation result and audio link.
    """
    payload = {
        "lyrics": lyrics,
        "tags": style_tags,
        "duration": duration,
    }

    try:
        result = ace_client.generate_music(payload)
        return f"Music generated successfully! Result: {result}"
    except Exception as e:
        return f"Generation failed (ACE-Step at {ACE_STEP_REMOTE_URL}): {e}"
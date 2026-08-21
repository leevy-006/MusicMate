import json
from pathlib import PurePosixPath
from urllib.parse import urljoin

from langchain_core.tools import tool
from config.settings import ACE_STEP_REMOTE_URL
from core.ace_step_client import ACEStepRemoteClient

ace_client = ACEStepRemoteClient(base_url=ACE_STEP_REMOTE_URL)


def _format_generation_result(result: dict) -> str:
    """Return a compact JSON payload that the web UI can render as audio cards."""
    raw_tracks = result.get("result", [])
    if isinstance(raw_tracks, str):
        try:
            raw_tracks = json.loads(raw_tracks)
        except json.JSONDecodeError:
            raw_tracks = []

    tracks = []
    for index, track in enumerate(raw_tracks if isinstance(raw_tracks, list) else [], 1):
        if not isinstance(track, dict) or not track.get("file"):
            continue

        file_url = track["file"]
        audio_url = urljoin(f"{ACE_STEP_REMOTE_URL.rstrip('/')}/", file_url.lstrip("/"))
        filename = PurePosixPath(file_url.split("?", 1)[0]).name or f"music-{index}.wav"
        metas = track.get("metas") or {}
        tracks.append({
            "index": index,
            "audio_url": audio_url,
            "filename": filename,
            "duration": metas.get("duration"),
            "bpm": metas.get("bpm"),
            "key": metas.get("keyscale"),
            "lyrics": track.get("lyrics") or metas.get("lyrics", ""),
            "status": track.get("stage", "succeeded"),
        })

    return json.dumps({
        "type": "music_generation",
        "status": result.get("status", "success"),
        "tracks": tracks,
    }, ensure_ascii=False)


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
        "audio_format": "wav",
    }

    try:
        result = ace_client.generate_music(payload)
        return _format_generation_result(result)
    except Exception as e:
        return json.dumps({
            "type": "music_generation",
            "status": "error",
            "error": f"Generation failed (ACE-Step at {ACE_STEP_REMOTE_URL}): {e}",
        }, ensure_ascii=False)
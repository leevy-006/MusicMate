import os
import unittest

from core.ace_step_client import ACEStepRemoteClient


class ACEStepToolConfigTest(unittest.TestCase):
    def test_settings_reads_ace_step_url_from_environment(self):
        os.environ["ACE_STEP_URL"] = "http://example.test:7860"

        from importlib import reload
        import config.settings

        reload(config.settings)
        self.assertEqual(config.settings.ACE_STEP_REMOTE_URL, "http://example.test:7860")

        os.environ.pop("ACE_STEP_URL", None)


class ACEStepResponseNormalizationTest(unittest.TestCase):
    def test_generate_music_accepts_list_like_query_results(self):
        client = ACEStepRemoteClient(base_url="http://example.test")
        client.release_task = lambda payload: "task-123"

        def fake_query_result(task_id):
            return [{"task_id": task_id, "status": "completed"}]

        client.query_result = fake_query_result

        result = client.generate_music({"lyrics": "demo", "tags": "pop"}, poll_interval=0, timeout=1)
        self.assertEqual(result, {"task_id": "task-123", "status": "completed"})


class GenerateMusicToolResultTest(unittest.TestCase):
    def test_generate_music_tool_extracts_stage_and_file(self):
        from core.tools import ace_client, generate_music

        fake_result = {
            "status": 1,
            "result": '[{"file": "/v1/audio?path=/workspace/audio.mp3", "stage": "succeeded"}]'
        }
        ace_client.generate_music = lambda payload: fake_result

        output = generate_music("lyrics", "pop", duration=120)
        self.assertIn("stage_1: succeeded", output)
        self.assertIn("file_1: /v1/audio?path=/workspace/audio.mp3", output)
        self.assertIn("audio_url_1:", output)


if __name__ == "__main__":
    unittest.main()

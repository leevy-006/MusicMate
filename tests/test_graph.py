import unittest

from agent.graph import MusicAgentGraph


class DummyCompiledGraph:
    def __init__(self):
        self.calls = []

    def invoke(self, *args, **kwargs):
        self.calls.append(("invoke", args, kwargs))
        return {"ok": True}

    def astream_events(self, *args, **kwargs):
        self.calls.append(("astream_events", args, kwargs))
        yield {"event": "done"}


class MusicAgentGraphTest(unittest.TestCase):
    def test_wrapper_delegates_to_compiled_graph(self):
        graph = MusicAgentGraph.__new__(MusicAgentGraph)
        compiled_graph = DummyCompiledGraph()
        graph.compiled_graph = compiled_graph

        result = graph.invoke({"messages": []}, config={"thread_id": "abc"})
        self.assertEqual(result, {"ok": True})
        self.assertEqual(compiled_graph.calls[0][0], "invoke")

        events = list(graph.astream_events({"messages": []}, config={"thread_id": "abc"}))
        self.assertEqual(events[0]["event"], "done")
        self.assertEqual(compiled_graph.calls[1][0], "astream_events")


if __name__ == "__main__":
    unittest.main()

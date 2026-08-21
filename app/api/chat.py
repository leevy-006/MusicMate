"""Chat API for MusicMate."""
import json
import uuid
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage
from agent.graph import MusicAgentGraph

router = APIRouter(tags=["chat"])

active_graphs: dict[str, MusicAgentGraph] = {}

def get_or_create_graph(session_id: str, provider: str) -> MusicAgentGraph:
    """Get an existing MusicAgentGraph for the session or create a new one."""
    if session_id not in active_graphs:
        active_graphs[session_id] = MusicAgentGraph(llm_provider=provider)
    return active_graphs[session_id]

@router.post("/chat")
async def chat(request: Request):
    """
    Streaming chat endpoint using Server-Sent Events.

    Request JSON body:
        {
            "session_id": "optional-uuid",
            "provider": "minimax",
            "message": "I want a chill lo-fi song about rain"
        }
    """
    body = await request.json()
    session_id = body.get("session_id", str(uuid.uuid4()))
    provider = body.get("provider", "minimax")
    user_message = body.get("message", "")

    if not user_message:
        return {"error": "message field is required"}

    graph_instance = get_or_create_graph(session_id, provider)
    config = {"configurable": {"thread_id": session_id}}

    async def event_generator():
        try:
            async for event in graph_instance.astream_events(
                {"messages": [HumanMessage(content=user_message)]},
                config=config,
                version="v2",
            ):
                kind = event["event"]

                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield {
                            "event": "token",
                            "data": json.dumps({"token": content}),
                        }

                elif kind == "on_tool_end":
                    tool_output = event["data"].get("output", "")
                    yield {
                        "event": "tool_result",
                        "data": json.dumps({"output": str(tool_output)}),
                    }

            yield {"event": "done", "data": json.dumps({"session_id": session_id})}

        except Exception as e:
            yield {"event": "error", "data": json.dumps({"error": str(e)})}

    return EventSourceResponse(event_generator())
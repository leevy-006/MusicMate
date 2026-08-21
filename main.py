# import sys
# import json
# import uuid
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, StreamingResponse
# from fastapi.staticfiles import StaticFiles
# from sse_starlette.sse import EventSourceResponse
# from langchain_core.messages import HumanMessage

# from agent.graph import MusicAgentGraph


# # ---------------------------------------------------------------------------
# # Global state
# # ---------------------------------------------------------------------------
# active_graphs: dict[str, MusicAgentGraph] = {}


# def get_or_create_graph(session_id: str, provider: str) -> MusicAgentGraph:
#     if session_id not in active_graphs:
#         active_graphs[session_id] = MusicAgentGraph(llm_provider=provider)
#     return active_graphs[session_id]


# # ---------------------------------------------------------------------------
# # FastAPI Application
# # ---------------------------------------------------------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Music Agent Server started.")
#     yield
#     print("Music Agent Server shutting down.")


# app = FastAPI(title="Music Agent API", lifespan=lifespan)


# @app.get("/", response_class=HTMLResponse)
# async def serve_frontend():
#     """Serve the single-page web UI."""
#     with open("server/web_ui.html", "r", encoding="utf-8") as f:
#         return HTMLResponse(content=f.read())


# @app.post("/api/chat")
# async def chat(request: Request):
#     """
#     Streaming chat endpoint using Server-Sent Events.

#     Request JSON body:
#         {
#             "session_id": "optional-uuid",
#             "provider": "minimax",
#             "message": "I want a chill lo-fi song about rain"
#         }
#     """
#     body = await request.json()
#     session_id = body.get("session_id", str(uuid.uuid4()))
#     provider = body.get("provider", "minimax")
#     user_message = body.get("message", "")

#     if not user_message:
#         return {"error": "message field is required"}

#     graph_instance = get_or_create_graph(session_id, provider)
#     config = {"configurable": {"thread_id": session_id}}

#     async def event_generator():
#         try:
#             # Stream tokens from the graph
#             async for event in graph_instance.astream_events(
#                 {"messages": [HumanMessage(content=user_message)]},
#                 config=config,
#                 version="v2",
#             ):
#                 kind = event["event"]

#                 # Capture LLM streaming tokens
#                 if kind == "on_chat_model_stream":
#                     content = event["data"]["chunk"].content
#                     if content:
#                         yield {
#                             "event": "token",
#                             "data": json.dumps({"token": content}),
#                         }

#                 # Capture tool execution results
#                 elif kind == "on_tool_end":
#                     tool_output = event["data"].get("output", "")
#                     yield {
#                         "event": "tool_result",
#                         "data": json.dumps({"output": str(tool_output)}),
#                     }

#             yield {"event": "done", "data": json.dumps({"session_id": session_id})}

#         except Exception as e:
#             yield {"event": "error", "data": json.dumps({"error": str(e)})}

#     return EventSourceResponse(event_generator())


# @app.get("/api/providers")
# async def list_providers():
#     """Return the list of available LLM providers."""
#     from config.settings import LLM_CONFIGS
#     return {"providers": list(LLM_CONFIGS.keys())}


# # ---------------------------------------------------------------------------
# # CLI Entry Point
# # ---------------------------------------------------------------------------
# def run_cli():
#     """Run the agent in terminal mode (no web UI)."""
#     print("=" * 50)
#     print("  Music Agent - Terminal Mode")
#     print("=" * 50)
#     print("\nAvailable LLM providers:")
#     from config.settings import LLM_CONFIGS
#     for i, name in enumerate(LLM_CONFIGS.keys(), 1):
#         print(f"  [{i}] {name}")

#     choice = input("\nSelect provider (number or name): ").strip()

#     # Resolve selection
#     providers = list(LLM_CONFIGS.keys())
#     if choice.isdigit() and 1 <= int(choice) <= len(providers):
#         selected = providers[int(choice) - 1]
#     elif choice.lower() in providers:
#         selected = choice.lower()
#     else:
#         print(f"Invalid selection. Defaulting to 'deepseek'.")
#         selected = "deepseek"

#     print(f"\nUsing provider: {selected}")
#     print("Type 'quit' or 'exit' to stop.\n")

#     graph_instance = MusicAgentGraph(llm_provider=selected)
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}

#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ("quit", "exit"):
#             print("Goodbye!")
#             break
#         if not user_input:
#             continue

#         try:
#             result = graph_instance.invoke(
#                 {"messages": [HumanMessage(content=user_input)]},
#                 config=config,
#             )
#             # Print the last AI message
#             ai_message = result["messages"][-1]
#             print(f"\nAgent: {ai_message.content}\n")
#         except Exception as e:
#             print(f"\nError: {e}\n")


# # ---------------------------------------------------------------------------
# # Main
# # ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     import uvicorn

#     if "--cli" in sys.argv:
#         run_cli()
#     else:
#         print("Starting Music Agent Web Server on http://localhost:8000")
#         uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)




import sys
import os


def main():
    """start the FastAPI server for MusicMate"""
    import uvicorn
    print("🎵 Starting MusicMate on http://localhost:8000")
    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


def run_cli():
    """start the CLI for MusicMate"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from agent import cli as cli_main
    cli_main()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        main()
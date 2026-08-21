# MusicMate

MusicMate is an AI-assisted music production agent built with FastAPI, LangGraph, LangChain, and a remote ACE-Step 1.5 music generation backend. It provides a web UI and CLI interface for composing song ideas, generating structured lyrics, selecting musical style tags, and invoking the ACE-Step music generation tool.

## Features

- Web-based chat interface for music creation
- Streaming AI responses using Server-Sent Events (SSE)
- Multiple LLM providers configured via `config/settings.py`
- Music generation via a remote ACE-Step 1.5 API
- LangGraph workflow orchestration for agent/tool interaction
- Simple CLI mode for terminal-based conversation

## Project Structure

- `server/main.py`: FastAPI application, SSE chat endpoint, provider listing, and CLI entry point
- `agent/graph.py`: LangGraph workflow builder for the music agent
- `agent/prompts.py`: System prompt guiding the music assistant behavior
- `core/llm_factory.py`: Factory for OpenAI-compatible LLM provider clients
- `core/tools.py`: Music generation tool wrapper around ACE-Step
- `core/ace_step_client.py`: Remote ACE-Step API client implementation
- `config/settings.py`: LLM provider configurations and ACE-Step URL settings
- `server/web_ui.html`: Single-page frontend for the chat UI
- `tests/test_graph.py`: Unit tests for the graph wrapper behavior

## Requirements

- Python 3.10+
- Install dependencies from `pyproject.toml`

## Environment Variables

The project uses `python-dotenv`. Create a `.env` file in the project root and define the following variables:

- `DEEPSEEK_API_KEY`
- `QWEN_API_KEY`
- `MINIMAX_API_KEY`
- `ACE_STEP_URL`
- `ACE_STEP_API_KEY` (optional, if the ACE-Step service requires a bearer token)

Example `.env`:

```env
DEEPSEEK_API_KEY=your_deepseek_key
QWEN_API_KEY=your_qwen_key
MINIMAX_API_KEY=your_minimax_key
ACE_STEP_URL=https://your-ace-step-host
ACE_STEP_API_KEY=your_ace_step_key
```

## Installation

Sync dependencies from `pyproject.toml` using `uv`:

```bash
uv sync
```

If you do not use `uv`, install dependencies manually from `pyproject.toml` or with a fallback `requirements.txt`.

## Running the Server

Run the web agent with `uv`:

```bash
uv run python -m server.main
```

Then open `http://localhost:8000` in your browser.

## Using the CLI

Run the terminal chat mode:

```bash
uv run python -m server.main --cli
```

## API Endpoints

### `POST /api/chat`

Start a streamed chat session. Request body:

```json
{
  "session_id": "optional-uuid",
  "provider": "deepseek",
  "message": "I want a chill lo-fi song about rain"
}
```

The endpoint returns an SSE stream with events:

- `token`: streaming text tokens from the AI
- `tool_result`: output returned by `generate_music`
- `error`: error messages
- `done`: session completion

### `GET /api/providers`

Returns the configured LLM provider list.

## LLM Providers

Configured providers in `config/settings.py`:

- `deepseek`
- `qwen`
- `minimax`

Each provider is mapped to an OpenAI-compatible model and base URL.

## Music Generation Flow

1. User sends a prompt through the chat UI or CLI
2. `MusicAgentGraph` builds a LangGraph workflow with an agent node and a tool node
3. The agent uses a system prompt in `agent/prompts.py` and may call `generate_music`
4. `core/tools.py` forwards the request to `ACEStepRemoteClient`
5. The ACE-Step API returns music generation results

## Notes

- The frontend is a lightweight static HTML page served from `server/web_ui.html`
- The chat UI uses SSE to display AI tokens incrementally
- `MusicAgentGraph` stores graph state via `MemorySaver`

## Testing

Run unit tests with:

```bash
python -m unittest tests/test_graph.py
```

## Customization

- Add or update LLM providers in `config/settings.py`
- Modify the system prompt in `agent/prompts.py` to change AI behavior
- Extend tool logic in `core/tools.py` for additional music generation workflows

## License

This project is currently unlicensed. Add a `LICENSE` file if you want to define reuse terms.

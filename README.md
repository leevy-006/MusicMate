# MusicMate
MusicMate is an AI-assisted music production agent. It uses LangGraph and LangChain to guide a conversation from song ideas to structured lyrics and style tags, then calls a remote ACE-Step 1.5 service to generate music.
The project includes:
- A FastAPI web server with a browser chat UI
- Streaming assistant responses over Server-Sent Events (SSE)
- Four selectable OpenAI-compatible LLM providers
- A LangGraph agent with the ACE-Step music generation tool
- A terminal CLI for provider selection and interactive chat
## Architecture
```text
Browser or CLI
  |
  v
FastAPI (app/server.py)
  |
  v
MusicAgentGraph (agent/graph.py)
  |
  +--> LLMFactory --> NVIDIA OpenAI-compatible endpoint
  |
  +--> generate_music --> remote ACE-Step 1.5 API
```
## Project Structure
```text
app/
  server.py                     FastAPI application
  api/chat.py                   Streaming chat endpoint
  api/providers.py              Provider list endpoint
  web/pages.py                  Serves the web UI
  web/web_ui.html               Browser chat interface
agent/
  graph.py                      LangGraph workflow and tool routing
  cli.py                        Terminal chat interface
  prompt_loader.py              Defines the music assistant system prompt
  prompts/music_agent.md        Prompt reference/documentation
core/
  llm_factory.py                OpenAI-compatible LLM factory
  tools.py                      ACE-Step generation tool
  ace_step_client.py            Async release/query ACE-Step client
config/settings.py              LLM and ACE-Step configuration
tests/                          Unit tests
docs/ace-step_api.md            ACE-Step API reference
```
## Requirements
- Python 3.10 or newer
- `uv` recommended for dependency management
- Access to the configured LLM API endpoints
- A running or reachable ACE-Step 1.5 API service
## Configuration
Create a `.env` file in the project root. The LLM configurations are defined in `config/settings.py` and use the NVIDIA OpenAI-compatible API endpoint by default.
```env
QWEN_API_KEY=your_qwen_key
DEEPSEEK_API_KEY=your_deepseek_key
MINIMAX_API_KEY=your_minimax_key
OPENAI_API_KEY=your_openai_key

ACE_STEP_URL=https://your-ace-step-host
ACE_STEP_API_KEY=your_ace_step_key
```
`ACE_STEP_API_KEY` is optional and is only needed when the ACE-Step server requires bearer-token authentication.
### Available LLM Providers

| Provider key | Model | Environment variable |
| --- | --- | --- |
| `qwen` | `Qwen/Qwen3-Next-80B-A3B-Instruct` | `QWEN_API_KEY` |
| `deepseek` | `deepseek-ai/deepseek-v4-flash-0731` | `DEEPSEEK_API_KEY` |
| `minimax` | `minimaxai/minimax-m3` | `MINIMAX_API_KEY` |
| `openAI` | `openai/gpt-oss-120b` | `OPENAI_API_KEY` |

All four providers currently use:

```text
https://integrate.api.nvidia.com/v1
```

Provider names are case-sensitive in the backend configuration. Use `openAI` exactly as shown.
## Installation
Install the project dependencies with `uv`:

```bash
uv sync
```
## Run the Web Application

Start the FastAPI server with:
```bash
uv run uvicorn app.server:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in a browser. The root page serves `app/web/web_ui.html`.
## Run the CLI

Start the terminal interface with:
```bash
uv run python -m agent.cli
```
The CLI lists the configured providers and accepts either a provider number or provider key. Type `quit` or `exit` to stop.
## API Endpoints

### `POST /api/chat`

Starts a streamed chat session. Request body:
```json
{
  "session_id": "optional-uuid",
  "provider": "minimax",
  "message": "Create a chill lo-fi song about rain"
}
```
The response is an SSE stream with these event types:
- `token`: an assistant response fragment
- `tool_result`: the ACE-Step generation result
- `error`: an error message
- `done`: the completed session ID

The server creates a graph for each session. When the provider changes for an existing `session_id`, a new graph is created for the new model.
### `GET /api/providers`

Returns the provider keys currently configured in `config/settings.py`:
```json
{
  "providers": ["qwen", "deepseek", "minimax", "openAI"]
}
```
## Music Generation

The assistant follows the workflow defined in `agent/prompt_loader.py`:
1. Understand the theme, mood, genre, and vocal requirements.
2. Generate structured lyrics using tags such as `[verse]` and `[chorus]`.
3. Confirm style tags such as genre, instruments, vocals, and BPM.
4. Call the `generate_music` tool.
5. Return the ACE-Step result and audio link.

`core/tools.py` sends the generation request to ACE-Step and explicitly requests WAV output with `audio_format: "wav"`. The ACE-Step API documentation is available at [docs/ace-step_api.md](docs/ace-step_api.md).
## Tests
Run the test suite with:
```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
```
You can also run the tests with pytest if it is installed:
```bash
uv run pytest
```

## Customization

- Add or change LLM providers in `config/settings.py`.
- Update the assistant behavior in `agent/prompt_loader.py`.
- Extend `core/tools.py` for additional music operations.
- Adjust the web interface in `app/web/web_ui.html`.
## License

This project currently has no license file.
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

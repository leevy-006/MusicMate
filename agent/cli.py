"""Run the agent in terminal mode (no web UI)."""
from agent.graph import MusicAgentGraph
from langchain_core.messages import HumanMessage
from config.settings import LLM_CONFIGS

print("=" * 50)
print("  Music Agent - Terminal Mode")
print("=" * 50)
print("\nAvailable LLM providers:")
for i, name in enumerate(LLM_CONFIGS.keys(), 1):
    print(f"  [{i}] {name}")

choice = input("\nSelect provider (number or name): ").strip()

providers = list(LLM_CONFIGS.keys())
if choice.isdigit() and 1 <= int(choice) <= len(providers):
    selected = providers[int(choice) - 1]
elif choice.lower() in providers:
    selected = choice.lower()
else:
    print(f"Invalid selection. Defaulting to 'deepseek'.")
    selected = "deepseek"

print(f"\nUsing provider: {selected}")
print("Type 'quit' or 'exit' to stop.\n")

graph_instance = MusicAgentGraph(llm_provider=selected)
session_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": session_id}}

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        print("Goodbye!")
        break
    if not user_input:
        continue

    try:
        result = graph_instance.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )
        ai_message = result["messages"][-1]
        print(f"\nAgent: {ai_message.content}\n")
    except Exception as e:
        print(f"\nError: {e}\n")
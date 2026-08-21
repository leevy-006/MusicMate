from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from core.llm_factory import LLMFactory
from core.tools import generate_music
from agent.prompt_loader import MUSIC_AGENT_SYSTEM_PROMPT


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class MusicAgentGraph:
    """Builds and compiles the LangGraph workflow for the music agent."""

    def __init__(self, llm_provider: str = "deepseek"):
        self.llm = LLMFactory.get_llm(llm_provider)
        self.tools = [generate_music]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.compiled_graph = self.build()

    def build(self):
        workflow = StateGraph(AgentState)

        def agent_node(state):
            messages = [SystemMessage(content=MUSIC_AGENT_SYSTEM_PROMPT)] + state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(self.tools))

        workflow.set_entry_point("agent")

        def should_continue(state):
            last_message = state["messages"][-1]
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return END

        workflow.add_conditional_edges(
            "agent", should_continue, {"tools": "tools", END: END}
        )
        workflow.add_edge("tools", "agent")

        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def invoke(self, *args, **kwargs):
        return self.compiled_graph.invoke(*args, **kwargs)

    def astream_events(self, *args, **kwargs):
        return self.compiled_graph.astream_events(*args, **kwargs)
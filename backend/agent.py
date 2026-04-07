from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os

from tools import search_flights, google_hotels, calculate_budget, update_trip_summary

# Load .env variables (like OPENAI_API_KEY)
load_dotenv()

# Load System Prompt
prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
try:
    with open(prompt_path, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "Bạn là trợ lý ảo."

# 1. State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Nodes
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
tools = [search_flights, google_hotels, calculate_budget, update_trip_summary]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Ensure system prompt is the first message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    print("---CALLING AGENT---")
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 3. Graph Construction
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

from langgraph.checkpoint.memory import MemorySaver

# Compile graph
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# 4. Interface (for testing via console if needed)
if __name__ == "__main__":
    import uuid
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    print("Welcome to TravelBuddy! Nhập 'quit' để thoát.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        events = graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="values"
        )
        for event in events:
            if "messages" in event:
                last_message = event["messages"][-1]
                if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                   print("TravelBuddy:", last_message.content)
                elif isinstance(last_message, AIMessage) and last_message.tool_calls:
                   for tc in last_message.tool_calls:
                       print(f"[{tc['name']} is being called]")
        print("-------")

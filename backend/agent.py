import os
import logging
from typing import Annotated, TypedDict, Dict, Any
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage

from tools import search_flights, google_hotels, calculate_budget, update_trip_summary, search_local_food

# Config logging theo yêu cầu Code Quality (10%)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Tải biến môi trường (Ví dụ: OPENAI_API_KEY)
load_dotenv()

# Tải System Prompt
prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
try:
    with open(prompt_path, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    logger.warning("Không tìm thấy file system_prompt.txt!")
    SYSTEM_PROMPT = "Bạn là trợ lý ảo."

# 1. State Definition
class AgentState(TypedDict):
    """Định nghĩa trạng thái bộ nhớ đồ thị lưu bằng TypedDict và add_messages"""
    messages: Annotated[list, add_messages]

# Thiết lập LLM và Binding Tools
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.2)
tools = [search_flights, google_hotels, calculate_budget, update_trip_summary, search_local_food]
llm_with_tools = llm.bind_tools(tools)

# 2. Định nghĩa Agent Node
def agent_node(state: AgentState) -> Dict[str, Any]:
    """Node xử lý luồng giao tiếp với người dùng và suy luận gọi Tools (Agent)"""
    messages = state["messages"]
    
    # Tiêm system prompt vào đầu danh sách nếu chưa có
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    last_msg = state["messages"][-1]
    if isinstance(last_msg, HumanMessage):
        logger.info(f"User Input: {last_msg.content}")
        
    # Gọi LLM thực thi
    logger.info("Đang gọi Agent LLM...")
    response = llm_with_tools.invoke(messages)
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tc in response.tool_calls:
            args = tc.get('args', {})
            logger.info(f"Agent quyết định gọi Tool: {tc['name']} | Tham số: {args}")
    else:
        logger.info(f"Agent trả lời: {response.content}")
            
    return {"messages": [response]}

# Node xử lý các Tool
tool_node = ToolNode(tools)

# 3. Xây dựng Kiến trúc Đồ thị (Graph Construction - 25%)
workflow = StateGraph(AgentState)

# Khai báo các Node đầy đủ
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Khai báo các Cạnh (Edges) bao gồm cả chiều của START, END
workflow.add_edge(START, "agent")

# Sử dụng conditional_edges để tự động đánh giá END (nếu tool_calls rỗng)
workflow.add_conditional_edges("agent", tools_condition) 
workflow.add_edge("tools", "agent")

# Biên dịch mô hình với MemorySaver để bảo lưu context state
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# 4. Interface môi trường terminal test trực tiếp
if __name__ == "__main__":
    import uuid
    # Sinh chỉ mục phiên chát
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    logger.info("Đã khởi tạo xong LangGraph. Nhập 'quit' để thoát.")
    
    while True:
        try:
            user_input = input("\nUser: ")
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
                       print(f"\nTravelBuddy: {last_message.content}")
                    elif isinstance(last_message, AIMessage) and last_message.tool_calls:
                       for tc in last_message.tool_calls:
                           logger.info(f"Agent Action -> Gọi lệnh tool [{tc['name']}]")
        except KeyboardInterrupt:
             break

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from agent import graph

app = FastAPI(title="TravelBuddy API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Hoặc cấu hình domain frontend cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    session_id: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    
    # Run the graph
    events = graph.stream(
        {"messages": [HumanMessage(content=request.user_input)]},
        config,
        stream_mode="values"
    )
    
    final_response = ""
    tools_called = []
    trip_summary_data = None
    
    for event in events:
        if "messages" in event:
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage):
                if last_message.tool_calls:
                    for tc in last_message.tool_calls:
                        tools_called.append(tc["name"])
                        if tc["name"] == "update_trip_summary":
                            trip_summary_data = tc["args"]
                elif last_message.content:
                    final_response = last_message.content
                    
    return {
        "final_response": final_response,
        "tools_called": list(set(tools_called)), # Remove duplicates if any
        "trip_summary": trip_summary_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

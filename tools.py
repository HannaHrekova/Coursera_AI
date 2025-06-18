from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import START, StateGraph
from retriever import load_guest_dataset, web_search_tool, youtube_qa_tool
from langchain_core.tools import Tool
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_huggingface.llms import HuggingFaceEndpoint
import os

# Weather Tool
def get_weather_info(location: str) -> str:
    """Fetches dummy weather information for a given location."""
    return f"The weather in {location} is currently sunny with 25°C."

weather_tool = Tool(
    name="weather_forecast",
    func=get_weather_info,
    description="Provides the current weather for a given location."
)

# Stats Tool
def get_hub_stats(topic: str) -> str:
    """Fetches the most downloaded model from a specific author on the Hugging Face Hub."""
    return f"Here are the latest statistics about {topic}: [Mocked data]"

statistics_tool = Tool(
    name="statistics_lookup",
    func=get_hub_stats,
    description="Provides statistical data about a given topic."
)

# List of tools
tools = [
    load_guest_dataset(),
    web_search_tool,
    youtube_qa_tool,
    weather_tool,
    statistics_tool
]

# LLM
llm_model = HuggingFaceEndpoint(
    repo_id="CohereLabs/c4ai-command-r-v01",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    inference_server_url="https://api-inference.huggingface.co/models/",
    temperature=0.5,
    max_new_tokens=2048
)

chat = ChatHuggingFace(llm=llm_model)

system_message_content = """
You are a helpful, general AI assistant named Alfred. Your primary goal is to answer user questions accurately and efficiently. Always use available tools if they can help answer the question. Never make up information. If you cannot answer using your tools, say "I don't know".

Here's how to use your tools:
1. 'load_guest_dataset': Use this tool to get information about specific guests. Example: "Who is Lady Ada Lovelace?" -> Call load_guest_dataset(guest_name='Lady Ada Lovelace')
2. 'web_search_tool': Use this tool for general web search when you need to find information that is not available in your specific datasets. Example: "What is the capital of France?" -> Call web_search_tool(query='capital of France')
3. 'youtube_qa_tool': Use this tool to get information from YouTube
4. 'weather_forecast': Use this tool to get current weather information for a specific location. Example: "What's the weather in London?" -> Call weather_forecast(location='London')
5. 'statistics_lookup': Use this tool to get statistical data about a given topic. Example: "Tell me statistics about AI advancements." -> Call statistics_lookup(topic='AI advancements')
Always consider using a tool if it's relevant to the user's query.
"""

# Bind tools to chat
chat_with_tools = chat.bind_tools(tools)

# Agent State
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

print("tools list:", tools)
for t in tools:
    print(type(t), getattr(t, "name", None))

# Assistant Node
def assistant(state: AgentState):
    messages_to_process = list(state["messages"])
    ai_message = chat_with_tools.invoke(messages_to_process)

    updated_messages = state["messages"] + [ai_message]
    
    return {
        "messages": updated_messages
    }

# Build LangGraph
builder = StateGraph(AgentState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant", 
    tools_condition, 
    {
        "tools": "tools",
        "__end__": "__end__"
    }
)
builder.add_edge("tools", "assistant")

alfred = builder.compile()

# Test invocation
# messages = [
#    SystemMessage(content=system_message_content),
#    HumanMessage(content="Tell me about our guest named 'Lady Ada Lovelace'.")
#]
#response = alfred.invoke({"messages": messages})

#print("🎩 Alfred's Response:")
#print(response['messages'][-1].content)


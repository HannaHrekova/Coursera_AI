import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tools import alfred

def chat_interface(message: str, history: list[list[str | None]]) -> str:
    
    langchain_messages = []

    for human_msg, ai_msg in history:
        if human_msg:
            langchain_messages.append(HumanMessage(content=human_msg))
        if ai_msg:
            langchain_messages.append(AIMessage(content=ai_msg))

    langchain_messages.append(HumanMessage(content=message))
    
    print(f"DEBUG: Messages sent to Alfred: {langchain_messages}")

    result = alfred.invoke({"messages": langchain_messages})

    final_ai_message = result["messages"][-1]

    if isinstance(final_ai_message, AIMessage):
        print(f"DEBUG: Final AI Message Content: '{final_ai_message.content}'")
        return final_ai_message.content
    elif final_ai_message.tool_calls:
        print(f"DEBUG: Agent ended with ToolCalls: {final_ai_message.tool_calls}")
        return "Alfred seems to have completed the tool challenge, but has not formulated a final answer. Try to clarify the question."
    else:
        print(f"DEBUG: Agent ended with unexpected message type: {type(final_ai_message)}. Content: {final_ai_message.content}")
        return "Alfred completed the work, but did not return the expected response."

iface = gr.ChatInterface(fn=chat_interface, title="🎩 Alfred - Your Gala Assistant")

if __name__ == "__main__":
    iface.launch()


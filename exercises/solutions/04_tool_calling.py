from langchain.messages import HumanMessage, ToolMessage
from langchain_ollama import ChatOllama

from science_tutor.tools import TOOLS

model = ChatOllama(model="qwen3.5:4b", temperature=0).bind_tools(TOOLS)
tool_map = {tool.name: tool for tool in TOOLS}

history = [HumanMessage(content="What science topics can I study?")]
ai_message = model.invoke(history)
history.append(ai_message)

for call in ai_message.tool_calls:
    result = tool_map[call["name"]].invoke(call["args"])
    history.append(ToolMessage(content=result, tool_call_id=call["id"]))

final = model.invoke(history)
print(final.content)

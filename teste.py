from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage, AIMessage

model = ChatOllama(base_url="http://127.0.0.1:11434", model="qwen3.5:4b", temperature=0, reasoning=False)
messages = [SystemMessage(content="Você é um tutor de ciências de ensino fundamental.")]

def chat(user_text: str) -> str:
    messages.append(HumanMessage(content=user_text))
    answer = model.invoke(messages)
    messages.append(answer)
    return str(answer.content)

print(chat("Hoje vou estudar ecossistemas."))

print("\n","=="*20,"\n")

print(chat("Qual tema eu disse que estou estudando?"))

for i, message in enumerate(messages, start=1):
    print(f"Mensagem {i}:")
    print(message.content)
    print("\n" + "==" * 20 + "\n")
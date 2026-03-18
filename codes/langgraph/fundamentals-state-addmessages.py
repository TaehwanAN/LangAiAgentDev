from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic

load_dotenv()

model = ChatAnthropic(model="claude-sonnet-4-6")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def chat_node(state: AgentState) -> dict:
    response = model.invoke(state["messages"])
    return {"messages": response}  # ← 오타 수정

graph = StateGraph(AgentState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Checkpointer로 멀티턴 세션 자동 관리
checkpointer = MemorySaver()
agent = graph.compile(checkpointer=checkpointer)

# thread_id로 대화 세션 구분 — 메시지를 직접 이어 붙일 필요 없음
config = {"configurable": {"thread_id": "teo-session-1"}}

state_1 = agent.invoke(
    {"messages": [HumanMessage(content="Hello, my name is Teo!")]},
    config=config
)
print("### 1st Turn ###")
print(state_1["messages"][-1].content)

state_2 = agent.invoke(
    {"messages": [HumanMessage(content="What is your favorite color?")]},
    config=config  # 같은 thread_id → 이전 대화가 자동으로 이어집니다
)
print("### 2nd Turn ###")
print(state_2["messages"][-1].content)
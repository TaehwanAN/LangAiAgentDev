from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

class MyGraphState(MessagesState):
  # messages: Annotated[list[AnyMessage], add_messages] --> included in MessagesState
  turn_count: int
  
def node_user(state:MyGraphState) -> dict:
  print("EXECUTING node_user")
  return {
    "messages": HumanMessage(content="Why Monterrey had so strong wind two days ago?")
  }

def node_ai(state:MyGraphState):
  print("EXECUTING node_ai")
  last_message = state["messages"][-1].content
  print(f"Human Message: {last_message}")
  
  response_content = f"I received {last_message}. I fake a response"
  return {
    "messages": AIMessage(content=response_content)
  }
  
def node_count(state:MyGraphState):
  print("EXECUTING node_count")
  return {
    "turn_count": state["turn_count"] +1
  }
  
graph = StateGraph(MyGraphState)
graph.add_node(node_user)
graph.add_node(node_ai)
graph.add_node(node_count)

graph.add_edge(START,"node_user")
graph.add_edge("node_user","node_ai")
graph.add_edge("node_ai","node_count")
graph.add_edge("node_count",END)

agent = graph.compile()
initial_state = {
  "turn_count": 0
}

final_state = agent.invoke(initial_state)

print("#"*90)
print(final_state)
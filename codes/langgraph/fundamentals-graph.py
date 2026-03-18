from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
load_dotenv()

# 1. Define a state
class SimpleState(TypedDict):
  messages: Annotated[list, add_messages]
  
graph = StateGraph(SimpleState)

# 2. Create nodes
def node_say_hello(state: SimpleState)->dict:
  print("Executing 'node_say_hello'")
  return {"messages":["Hello"]}
def node_say_world(state: SimpleState)->dict:
  print("Executing 'node_say_world'")
  return {"messages":["World"]}

graph.add_node("hello-node",node_say_hello)
graph.add_node("world-node",node_say_world)

# 3. Link nodes with edges
graph.add_edge(START, "hello-node")
graph.add_edge("hello-node","world-node")
graph.add_edge("world-node",END)

# 4. Compile Graph
agent = graph.compile() # Runnable

# 5. Run the Graph
initial_state = {
  "messages": []
}
final_state = agent.invoke(initial_state)

print(final_state)
# print(agent.get_graph())
print(agent.get_graph().draw_ascii())
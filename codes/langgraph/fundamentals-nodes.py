from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
  input: str
  execution_path: list[str]
  
def node_a(state:GraphState) -> dict:
  print("### node_a EXECUTING ---")
  new_path = state.get("execution_path",[]) + ["node_a"]
  return {
    "execution_path": new_path
  }
  
def node_b(state:GraphState) -> dict:
  print("### node_b EXECUTING ---")
  new_path = state.get("execution_path", []) + ["node_b"]
  return {
    "execution_path": new_path
  }
  
def node_c(state:GraphState) -> dict:
  print("### node_c EXECUTING ---")
  new_path = state.get("execution_path", []) + ["node_c"]
  return {
    "execution_path": new_path
  }
  
def node_d(state:GraphState) -> dict:
  print("### node_d EXECUTING ---")
  new_path = state.get("execution_path", []) + ["node_d"]
  return {
    "execution_path": new_path
  }
  
def branch_c_or_d(state:GraphState):
  print("Evaluating Conditional Edge")
  
  if "go_to_c" in state["input"]:
    return "node_c"
  else:
    return "node_d"
  
builder = StateGraph(GraphState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_d)

builder.add_edge(START,"node_a")
builder.add_edge("node_a","node_b")

###
builder.add_conditional_edges("node_b",branch_c_or_d)

builder.add_edge("node_c", END)
builder.add_edge("node_d", END)

graph = builder.compile()

state_init_1 = {
  "input": "Hello, Langraph is Awesome"
}
state_final = graph.invoke(state_init_1)
print("#"*100)
print(state_final)

state_init_2 = {
  "input": "Hello, World. go_to_c"
}
state_final = graph.invoke(state_init_2)
print("#"*100)
print(state_final)
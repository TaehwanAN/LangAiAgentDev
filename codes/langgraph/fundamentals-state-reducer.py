from typing import Annotated, List, TypedDict

from langgraph.graph import StateGraph, END, START

class StateWithoutReducer(TypedDict):
  count: int
  animals: List[str]
  
def node_to_update(state:StateWithoutReducer) -> dict:
  return {
    "count": 11, "animals": ["cat","dog"]
  }

def run_example(name: str, state_schema: type, node_func: callable, initial_state: dict):
  """
  Build and run a simple graph with a given state schema, node, and initial state
  """
  print(f"### Running Example: {name} ###")
  graph = StateGraph(state_schema)
  graph.add_node("update_node", node_func)
  graph.add_edge(START, "update_node")
  graph.add_edge("update_node",END)
  
  app = graph.compile()
  
  final_state = app.invoke(initial_state)
  
  print("### Initial State: ###")
  for k,v in initial_state.items():
    print(f"#### {k}: {v} ####")
  print("### Final State: ###")
  for k,v in final_state.items():
    print(f"#### {k}: {v} ####")


initial_state = {"count":84, "animals": ["lion","buffalo"]}

run_example(
  name = "no reducer", state_schema=StateWithoutReducer,initial_state=initial_state,node_func=node_to_update
)

# With Reducer
def update_count(current,new):
  return current + new
def update_animals(current:List[str], new:List[str]) -> List[str]:
  return current + new

class StateWithReducer(TypedDict):
  count: Annotated[int, update_count]
  animals: Annotated[List[str],update_animals]

run_example(
  name = "yes reducer", state_schema=StateWithReducer,initial_state=initial_state,node_func=node_to_update
)
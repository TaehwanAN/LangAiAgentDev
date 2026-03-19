from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class GraphState(TypedDict):
  temperature: int
  status_message: str
  warning_sent: bool
  final_action_performed: str
  
def node_get_temperature(state: GraphState) -> Command[Literal["warn_user","success"]]:
  temperature = state["temperature"]
  if temperature > 90:
    print("Alert: Temperature too high!")
    return Command(
      update= {"status_message": "Routing to warning handler...", "warning_sent": True},
      goto = "warn_user"
    )
  else:
    print("OK: Temperature is fine")
    return Command(
      update= {"status_message": "Routing to success handler..."},
      goto="success"
    )
    
def warn_user(state:GraphState):
  print(f"Executin warn user. Temperature: {state['temperature']}")
  return {
    "warning_sent": True, "final_action_performed": "Warning norification sent"
  }
def success(state:GraphState):
  print(f"Executin successr. Temperature: {state['temperature']}")
  return {
    "final_action_performed": "Temp saftety confirmed"
  }
  
builder = StateGraph(GraphState)
builder.add_node(node_get_temperature)
builder.add_node(warn_user)
builder.add_node(success)

builder.add_edge(START,"node_get_temperature")

graph = builder.compile()

state_init = {"temperature": 999}

state_final = graph.invoke(state_init)
print("Final STATE:")
print(state_final)

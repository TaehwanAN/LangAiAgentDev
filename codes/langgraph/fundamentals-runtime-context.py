from dataclasses import dataclass
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

class GraphState(TypedDict):
  input:str
  result:str
  
@dataclass
class MyGraphContext:
  user_agent: str
  docs_url: str = "https://docs.langchain.com"
  db_connection: str = "mysql://user:password@localhost:3306/my_db"
  
def node_accessing_runtime_context(state: GraphState, runtime:Runtime[MyGraphContext]):
  print("### EXECUTING node")
  db_string = runtime.context.db_connection
  docs_url = runtime.context.docs_url
  user_agent = runtime.context.user_agent
  
  print(f"Current DB String: {db_string}")
  print(f"Documentation URL: {docs_url}")
  print(f"User Agent: {user_agent}")
  
builder = StateGraph(GraphState, context_schema=MyGraphContext)
builder.add_node("node_accessing_runtime_context",node_accessing_runtime_context)
builder.add_edge(START,"node_accessing_runtime_context")
builder.add_edge("node_accessing_runtime_context",END)

graph = builder.compile()

state_init = {"input": "Start Process"}
state_final = graph.invoke(
    state_init,
    context=MyGraphContext(user_agent="Mozilla/5.0 (course-demo)")
)

print("final state")
print(state_final)
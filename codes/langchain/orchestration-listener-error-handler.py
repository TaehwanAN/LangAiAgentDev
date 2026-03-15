from langchain_core.runnables import RunnableLambda
from typing import Any, Dict
import json
from langchain_core.tracers.schemas import Run

def handler_error(input_dict:Dict[str,Any]) -> str:
  topic:str = input_dict.get("topic", "NOT FOUND")
  
  lower_topic = topic.lower()
  
  if "error" in lower_topic:
    raise ValueError(f"Intentioanal Error - Triggered by Topic: {topic}")
  elif "network" in lower_topic:
    raise ConnectionError(f"Simulated Network Connection Failure")
  elif "json" in lower_topic:
    bad_json = '{"incomplete": json}'
    return json.loads(bad_json)
  else:
    return f"Processing Topic: {topic}"

error_runnable = RunnableLambda(handler_error)

def listener_on_error(run: Run):
  print(f"Run ID: {run.id}")
  print(f"Run name: {run.name}")
  print(f"Started: {run.start_time} / Ended: {run.end_time}")
  print(f"Input: {run.inputs} / Output: {run.outputs}")
  print("--- Error Details ---")
  print(run.error)
  
error_runnable_with_listener = error_runnable.with_listeners(
  on_error=listener_on_error
)

print("------------ DEMO: Running Error Scenario -------------")

try:
  result = error_runnable_with_listener.invoke(
    {"topic": "error somewhere here"}
  )
  print(f"Result: {result}")
except Exception as e:
  print("An Error Occurred")
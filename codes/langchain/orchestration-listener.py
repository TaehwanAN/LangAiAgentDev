from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers.schemas import Run
from dotenv import load_dotenv
load_dotenv()

model = ChatAnthropic(model="claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_template("Give me a simple short fact about {topic}")

fact_chain = prompt | model | StrOutputParser()

def listner_on_start(run: Run):
  print(f"Listner START ON START: {run.name} (Run ID: {run.id})")
  print(f"Inputs: {run.inputs}")
  print(f"Parent Run ID: {run.parent_run_id}")
  print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata','')}")
  
def listner_on_end(run: Run):
  print(f"Listner START ON END: {run.name} (Run ID: {run.id})")
  print(f"Outputs: {run.outputs}")
  print(f"Parent Run ID: {run.parent_run_id}")
  print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata','')}")
  
fact_chain_with_listners = fact_chain.with_listeners(
  on_start=listner_on_start,on_end=listner_on_end
)

result = fact_chain_with_listners.invoke(
  {
    "topic": "the Mexican Corruption"
  }
)

print(f"### Final Result: {result}")
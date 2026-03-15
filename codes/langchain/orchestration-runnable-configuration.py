"""
langchain_core.runnables RunnableCofig
주요 파라미터
  run_name: str -> 실행의 이름을 명시적으로 지정. LangSmith 추적 시 전체 체인이 아닌 해당 실행 단위 식별.
  max_concurrency: int -> batch 호출 시, 동시에 실행할 최대 작업 수 제한. API Rate Limit 피할때 필수.
  recursion_limit: int -> 깊이 제한. 재귀적 Runnable의 무한 루프 방지.
  callbacks: List[BaseCallbackHandler] -> 로그출력, 파일저장, 스트리밍데이터 전송 등 실행 중 발생하는 이벤트를 가로채는 핸들러 객체.
  return_intermediate_steps: bool -> 체인의 중간 결과들을 리턴할지
  tags: List[str] -> 
  configurable: dict -> 
"""
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers.schemas import Run

load_dotenv()

model = ChatAnthropic( model = "claude-sonnet-4-6")
prompt = ChatPromptTemplate.from_template("Tell me fact only about {topic}.")
parser = StrOutputParser()

base_chain = prompt | model | parser

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
  
base_chain_with_listeners = base_chain.with_listeners(
  on_start=listner_on_start,on_end=listner_on_end
)

runnable_config_per_invoke = RunnableConfig(
  run_name = "Runnable Configuration Per-Invoke DEMO",
  tags = ['single_run','demo'],
  metadata= {
    "user_id": "my_user_id","source": "my_source_test", "input_topic_type": "history"
  }
)


print("--- Demo 1: Per-Invocation Configuration ---")
# per_invoke_result = base_chain_with_listeners.invoke(
#   {
#     "topic": "Iran"
#   },
#   config=runnable_config_per_invoke
# )
# print(per_invoke_result)

print("--- Demo 2: Persistent Configuration ---")
runnable_config_persistent = RunnableConfig(
  run_name="Runnable Configuration Persisten DEMO",
  tags = ["persistent","demo"],
  metadata= {
    "user_id": "my_user_id","source": "my_source_test", "input_topic_type": "history"
  }
)
persistent_chain = base_chain_with_listeners.with_config(runnable_config_persistent)
persistent_result = persistent_chain.invoke(
  {"topic":"Spiders"}
)
print("#"*100)
print(persistent_result)
print("#"*100)


from langchain_core.runnables import RunnableParallel, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

runnable_1 = RunnableLambda(lambda input: str(input).upper())
runnable_2 = RunnableLambda(lambda input: str(input).lower())
runnable_3 = RunnableLambda(lambda input: str(input).replace(" ","",-1))

# Demo 1 - Dict
parallel_1 = RunnableParallel(
  {
    "uppercase": runnable_1, "lowercase": runnable_2, "removespace": runnable_3
  }
)

result_1 = parallel_1.invoke("Hello World! !")
print(result_1)

# Demo 2 - Kwargs
parallel_2 = RunnableParallel(
  first = runnable_1,
  second = runnable_2,
  third = runnable_3,
  last = runnable_1
)

result_2 = parallel_2.invoke("Hello World! !")
print(result_2)

# Demo 3 - LCEL
parallel_3 = parallel_2 | (lambda x: x['first'] + " | " + x['second'] )
result_3 = parallel_3.invoke("Hello World! !")
print(result_3)

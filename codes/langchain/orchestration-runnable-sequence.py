from langchain_core.runnables import RunnableLambda, RunnableSequence

runnable_1 = RunnableLambda(lambda input: input + 5)
runnable_2 = RunnableLambda(lambda input: input * 3)
runnable_3 = RunnableLambda(lambda input: input / 15)
runnable_4 = RunnableLambda(lambda input: input -50)

# Demo 1 - RunnableSequece
sequence_1 = RunnableSequence(
  first=runnable_2,
  middle=[runnable_1,runnable_3,runnable_2],
  last = runnable_4
)

result_1 = sequence_1.invoke(100)
print(result_1)

# Demo 2 - pipe()
sequence_2 = runnable_1.pipe(runnable_4)
result_2 = sequence_2.invoke(50)
print(result_2)

# Demo 3 - LCEL (|)
sequence_3 = runnable_1|runnable_3|runnable_4|runnable_1
result_3 = sequence_3.invoke(516)
print(result_3)
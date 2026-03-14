from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(
  model = "claude-haiku-4-5"
)


# 1 - invoke
invoked_prompt = "where is the eiffel tower"
response = model.invoke(invoked_prompt)
print("1. Runnable Invoke")
print(response)
print()

# 2 - batch
batched_prompt_list = [
  "where is the great wall",
  "where is the pyramid",
  "where is the statue of liberty"
]
response = model.batch(batched_prompt_list)
response_list = [r.content for r in response]
print("2. Runnable Batch")
print(response_list)
print()

# 3 - stream
stream_prompt = "where is the chikichikichakachakacho"
response = model.stream(stream_prompt)
print("3. Runnable Stream")
for chunk in response:
  print(chunk.content, end="", flush=True)
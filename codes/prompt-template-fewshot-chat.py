from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model ='claude-sonnet-4-6')

example_formatter = ChatPromptTemplate.from_messages(
  [
    ("human","{input}"),
    ("ai","{output}"),
  ]
)

example_set = [
  {"input":"2 ribbit 2", "output":"4"},
  {"input":"332 ribbit 13", "output":"345"},
  {"input":"98 ribbit 2", "output":"100"},
]

few_shot_template = FewShotChatMessagePromptTemplate(
  example_prompt=example_formatter, examples=example_set
)
print(few_shot_template,end="\n\n\n")

main_prompt = ChatPromptTemplate.from_messages(
  [
    ("system","You are a whimsical mathematician"),
    few_shot_template,
    ("human","{user_prompt}")
  ]
)
print(main_prompt,end="\n\n\n")

invoked_prompt = main_prompt.invoke(
  {"user_prompt":"1535135 ribbit 309809"}
)
print(invoked_prompt, end="\n\n\n")
print(invoked_prompt.to_string())

# response = model.invoke(invoked_prompt)
# print(response)

# LCEL - LangChain Expression Language
chain = main_prompt | model
response = chain.batch(
  [
    {"user_prompt":"123 ribbit 456"},
    {"user_prompt":"123 ribbit 456 ribbit 789"},
    {"user_prompt": "abcdww ribbit xyz"}
  ]
)

for res in response:
  print(res.content)

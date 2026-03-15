from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField, RunnableConfig


load_dotenv()

# model.configurable_fields
model = ChatAnthropic( model = "claude-sonnet-4-6").configurable_fields(
  max_tokens = ConfigurableField(
    id = "llm_token_cap",
    name = "LLM Maximum Response Tokens",
    description= "Number of maximum tokens to be used for response"
  )
)


prompt = ChatPromptTemplate.from_template("Tell me fact only about {topic}.")
parser = StrOutputParser()

base_chain = prompt | model | parser

print("--- Invoking with default token limit ---")
result_default_token = base_chain.invoke({
  "topic": "the sun"
})
print(f"Fact about the sun (Max Tokens = default): {result_default_token}")

print("--- Invoking with a low token limit ---")
low_tokens_config = RunnableConfig(
  configurable={
    "llm_token_cap": 10
  }
)
result_low_token = base_chain.invoke(
  {
    "topic": "the sun"
  },
  config=low_tokens_config
)

print(f"Fact about the sun (Max Tokens = low): {result_low_token}")
print()
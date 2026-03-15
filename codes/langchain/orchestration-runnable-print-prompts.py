from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

model = ChatAnthropic(
  model = 'claude-sonnet-4-6'
)


prompt = ChatPromptTemplate.from_template("Write a short, concise sentence about {topic}")

output_parser = StrOutputParser()

simple_chain = prompt | model | output_parser

# result = simple_chain.invoke(
#   {
#     "topic":"Functional Programming"
#   }
# )
# 
# print(result)

# Demo 2- Chain to Runnable
combined_chain = simple_chain | (lambda chain_output: chain_output + "Oh, wow. That's awesome!!" )

# Demo 3 - Chain to Chain
# invoke -> receive result -> using the result, invoke again
fact_checking_prompt = ChatPromptTemplate.from_messages(
  [
    ("system","Start by quoting the statement, then give the reason"),
    ("user","How much correct is this statement: {statement}")
  ]
)

checker_chain = fact_checking_prompt | model | output_parser

fact_check_result = {"statement": simple_chain} | checker_chain

all_prompts = fact_check_result.get_prompts()

for i,p in enumerate(all_prompts):
  print(f"--- Prompt No.{i+1} ---")
  print(p.pretty_repr())
  print("-"*45, end="\n")

# dual_chain_result = fact_check_result.invoke(
#   {"topic": "Prompt Engineering"}
# )
# print("--- Dual Chain Output ---")
# print(dual_chain_result)

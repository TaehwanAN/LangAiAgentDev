# Construct Prompts

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

model = ChatAnthropic(model='claude-haiku-4-5')

# PromptTeamplate
prompt_1 = PromptTemplate(template="What is the capital of South Korea?") 
prompt_2 = PromptTemplate.from_template("What is the capital of South Korea?") # Recommended


print(prompt_2.invoke(
    {}
)) # text='What is the capital of South Korea?'

print(prompt_2.format()) # What is the capital of South Korea?


prompt_3 = PromptTemplate.from_template("What is the capital of {country}?")
print(prompt_3.invoke(
    {'country': "India"}
))
print(prompt_3.format(country="India"))


# response = model.invoke(prompt_3.invoke({"country":"Germany"}))
# print(response)

# ChatPromptTemplate
prompts = [
    ("system","Reply every prompts in {language}."), ("user", "Who is the president of {country}?")
]
chat_prompt = ChatPromptTemplate(prompts)
# print(chat_prompt.invoke({})) # messages=[SystemMessage(content='Reply every prompts in Spanish.', additional_kwargs={}, response_metadata={}), HumanMessage(content='Who is the president of South Korea?', additional_kwargs={}, response_metadata={})]

req_prompt = chat_prompt.invoke(
    {
        "country": "China",
        "language": "Japanese"
    }
)

response = model.invoke(req_prompt)
print(response)

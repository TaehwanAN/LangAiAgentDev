from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate

load_dotenv() 

prompts = [
  ("system","You are a helpful assistant that gives straight-forward answers."),
  ("human","Who is the president of {country}?"),
  ("ai","{answer}"),
  ("human","What are the political promises of {the_president}?")
]

chat_prompt_template = ChatPromptTemplate(messages=prompts)
chat_prompt = chat_prompt_template.invoke({
  "country": "USA",
  "answer": "Donald Trump",
  "the_president": "the president"
})

# print(chat_prompt)
print(chat_prompt.to_string)
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

# model = ChatOpenAI(model='gpt-4')
model = ChatAnthropic(model='claude-haiku-4-5')

# Prompts
prompt_1 = "Who is the president of Mexico?"
prompt_2 = "What is the capital of Mexico?"
prompt_3 = "What is the most popular sport in Mexico?"

# Adding Prompts
prompts_list = list()
prompts_list.append(prompt_1)
prompts_list.append(prompt_2)
prompts_list.append(prompt_3)

# get response
response = model.batch(prompts_list)

# print(response)
for i, res in enumerate(response):
    print(f"{i+1} response: ")
    print(res)
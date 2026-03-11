from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

# model = ChatOpenAI(model='gpt-4')
model = ChatAnthropic(model='claude-sonnet-4-6')

response = model.invoke('Who is the president of France?')

print(response)
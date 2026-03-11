# Construct Prompts

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage # User Message
from langchain_core.messages import SystemMessage # System Message

load_dotenv()
model = ChatAnthropic(model='claude-haiku-4-5')

system_msg = SystemMessage(content='Reply every prompt in Spanish.')
user_msg = HumanMessage(content= 'Who is the president of Argentina?')

response = model.invoke(
    [
        system_msg,user_msg
    ]
)

print(response)
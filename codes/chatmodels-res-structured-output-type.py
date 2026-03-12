from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

from langchain_anthropic import ChatAnthropic

load_dotenv()

model = ChatAnthropic(
  model = 'claude-sonnet-4-6',
  temperature=0.1
)

class President(BaseModel):
  """detail information about the president"""
  
  name: str = Field(description="name of president")
  country: str = Field(description="country of president")
  age: Optional[int] = Field(description="age of president", default=None)
  political_ideology: str = Field(description="political ideaology or stance of president")

structured_model = model.with_structured_output(President)

response = structured_model.invoke("Who is the president of USA?")

print(response)
# name='Joe Biden' country='USA' age=82 political_ideology='Liberal/Progressive (Democratic Party)'
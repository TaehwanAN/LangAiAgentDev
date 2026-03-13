from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

string_prompt_1 = PromptTemplate(
    template = "Write a poem about Python"
)
actual_prompt_1 = string_prompt_1.invoke({})
print(string_prompt_1)
print(actual_prompt_1)


string_prompt_2 = PromptTemplate.from_template("Write a poem about {programming_language}")
actual_prompt_2 = string_prompt_2.invoke({"programming_language":"JavaSctipt"})
print(string_prompt_2)
print(actual_prompt_2)


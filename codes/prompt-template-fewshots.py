from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

template = "Question: {question}\nAnswer: {answer}"

prompt_template = PromptTemplate.from_template(template=template)

examples = [
  {"question":"Tell me about the US", "answer":"Continent: North America | President: Donald Trump | Language: English"},
  {"question":"Tell me about the Mexico", "answer":"Continent: Central America | President: Claudia Sheinbaum | Language: Spanish"},
  {"question":"Tell me about the US", "answer":"Continent: Asia | Leader: Kim Jeong Eun | Language: Korean"},
]

few_shot_prompt_template = FewShotPromptTemplate(
  example_prompt = template, examples = examples, suffix="Question: {user_query}"
)

invoked_template = few_shot_prompt_template.invoke(
  {"user_query": "Who built the great wall of China"}
)

print(invoked_template)
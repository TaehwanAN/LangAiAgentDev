from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", api_key="")

response = model.invoke(input="Where is the Statue of Liberty")

print(response.content)
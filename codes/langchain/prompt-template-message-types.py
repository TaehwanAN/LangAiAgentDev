from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

# Class Syntax
# user_msg = HumanMessage(content = "Write a poem about spring's sadness")
# prompt = [user_msg]

# Short-Hand Syntax
# prompt = [
#     ("System","Reply me in Spanish"),
#     ("human","Write a poem about spring's sadness")
# ]

# Dynamic Message
prompt = [
    ("System","Reply me in {language}"),
    ("human","Write a poem about {topic}")
]

print(prompt)

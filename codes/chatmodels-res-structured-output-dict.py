from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic

load_dotenv()

model = ChatAnthropic(
  model = 'claude-sonnet-4-6',
  temperature=0
)

president_info_schema = {
  "name": "president_info_schema",
  "description": "Gets information about the president.",
  "parameters": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string","description": "The name of the president"
      },
      "country": {
        "type": "string","description": "The country that the president represents"
      },
      "age": {
        "type": ["integer","null"], "description": "The age of the president"
      },
      "political-ideology": {
        "type": ["string","null"], "description": "The political ideology that the president shows"
      }
    },
    "required": ["name","country","political-ideology"]
  }
}

structured_model = model.with_structured_output(president_info_schema)

response = structured_model.invoke("Who is the president of South Korea?")

print(response)
# {'name': 'Yoon Suk-yeol', 'country': 'South Korea', 'political-ideology': 'Conservative'}
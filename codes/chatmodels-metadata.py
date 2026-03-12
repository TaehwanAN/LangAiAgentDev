from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

# model = ChatOpenAI(model='gpt-4')
model = ChatAnthropic(model='claude-haiku-4-5')

response = model.invoke("Who is the president of Israel?")
print(response.usage_metadata)
# {'input_tokens': 14, 'output_tokens': 62, 'total_tokens': 76, 'input_token_details': {'cache_read': 0, 'cache_creation': 0, 'ephemeral_5m_input_tokens': 0, 'ephemeral_1h_input_tokens': 0}}

print(response.response_metadata)
# {'id': 'msg_01AeqQUdvg5La7jhF3YK69TP', 'container': None, 'model': 'claude-haiku-4-5-20251001', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'cache_creation': {'ephemeral_1h_input_tokens': 0, 'ephemeral_5m_input_tokens': 0}, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'inference_geo': 'not_available', 'input_tokens': 14, 'output_tokens': 61, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-haiku-4-5-20251001', 'model_provider': 'anthropic'}
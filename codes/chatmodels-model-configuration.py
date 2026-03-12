import os

from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic


load_dotenv()

model = ChatAnthropic(
  model = 'claude-haiku-4-5',
  api_key= os.environ.get("ANTHROPIC_API_KEY"),
  max_tokens_to_sample=50
)

response = model.invoke("Explain the current war between Iran and USA.")

print(response) # content="# Iran-U.S. Tensions: Current Status\n\nThere's no active large-scale war, but significant tensions exist:\n\n## Recent Escalations (2024)\n- **April 2024**: Iran launched ~300 " additional_kwargs={} response_metadata={'id': 'msg_01PYPaKrriBS4HJEdDXbrzd7', 'container': None, 'model': 'claude-haiku-4-5-20251001', 'stop_reason': 'max_tokens', 'stop_sequence': None, 'usage': {'cache_creation': {'ephemeral_1h_input_tokens': 0, 'ephemeral_5m_input_tokens': 0}, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'inference_geo': 'not_available', 'input_tokens': 17, 'output_tokens': 50, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-haiku-4-5-20251001', 'model_provider': 'anthropic'} id='lc_run--019cdff4-5656-73d1-ac50-389285f10e13-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 17, 'output_tokens': 50, 'total_tokens': 67, 'input_token_details': {'cache_read': 0, 'cache_creation': 0, 'ephemeral_5m_input_tokens': 0, 'ephemeral_1h_input_tokens': 0}}

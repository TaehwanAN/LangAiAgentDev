"""
- How
  1. Identify the cache storage to use(memory or database)
  2. Use langchain's 'set_llm_cache' to set it as your response caching layer
"""

from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

load_dotenv()

model = ChatAnthropic(
  model = 'claude-sonnet-4-6'
)

set_llm_cache(InMemoryCache())

prompt = "Who is the president of Nigeria?"

response_1 = model.invoke(prompt)
response_2 = model.invoke(prompt)

print(response_1)
print(response_2)

"""
content='As of my knowledge cutoff in early 2025, the president of Nigeria is **Bola Tinubu**, who took office on May 29, 2023. For the most current information, I recommend checking a recent news source.' additional_kwargs={} response_metadata={'id': 'msg_01Uuwi5sQzWxUemxQJkmTyfp', 'container': None, 'model': 'claude-sonnet-4-6', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'cache_creation': {'ephemeral_1h_input_tokens': 0, 'ephemeral_5m_input_tokens': 0}, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'inference_geo': 'global', 'input_tokens': 14, 'output_tokens': 55, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-sonnet-4-6', 'model_provider': 'anthropic'} id='lc_run--019ce051-a535-7772-9bfb-9d2ce3147fb5-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 14, 'output_tokens': 55, 'total_tokens': 69, 'input_token_details': {'cache_read': 0, 'cache_creation': 0, 'ephemeral_5m_input_tokens': 0, 'ephemeral_1h_input_tokens': 0}}
content='As of my knowledge cutoff in early 2025, the president of Nigeria is **Bola Tinubu**, who took office on May 29, 2023. For the most current information, I recommend checking a recent news source.' additional_kwargs={} response_metadata={'id': 'msg_01Uuwi5sQzWxUemxQJkmTyfp', 'container': None, 'model': 'claude-sonnet-4-6', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'cache_creation': {'ephemeral_1h_input_tokens': 0, 'ephemeral_5m_input_tokens': 0}, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'inference_geo': 'global', 'input_tokens': 14, 'output_tokens': 55, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-sonnet-4-6', 'model_provider': 'anthropic'} id='lc_run--019ce051-a535-7772-9bfb-9d2ce3147fb5-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 14, 'output_tokens': 55, 'total_tokens': 69, 'input_token_details': {'cache_read': 0, 'cache_creation': 0, 'ephemeral_5m_input_tokens': 0, 'ephemeral_1h_input_tokens': 0}, 'total_cost': 0}
"""

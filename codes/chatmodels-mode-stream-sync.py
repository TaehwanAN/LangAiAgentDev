# Construct Prompts

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic



load_dotenv()

model = ChatAnthropic(model='claude-sonnet-4-6', max_tokens_to_sample=128)

streamed_response = model.stream("Tell me about the winners of the Novel Prize in 2023")

# for chunk in streamed_response:
#   print(chunk, flush=True)
"""
content='' additional_kwargs={} response_metadata={'model_name': 'claude-sonnet-4-6', 'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content='##' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' Nobel' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' Prize Winners' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' ' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content='2023\n\nHere' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' are the laure' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
...
content=' Physiology or Medicine\n**Katal' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content='in Karikó and' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' Drew' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content=' We' additional_kwargs={} response_metadata={'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] tool_call_chunks=[]
content='' additional_kwargs={} response_metadata={'stop_reason': 'max_tokens', 'stop_sequence': None, 'model_provider': 'anthropic'} id='lc_run--019ce015-f91c-7bd2-b032-0226f69a0622' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 20, 'output_tokens': 128, 'total_tokens': 148, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}} tool_call_chunks=[] chunk_position='last'
"""

for chunk in streamed_response:
  print(chunk.content, end="|")
"""
|##| Nobel| Prize Winners| |2023

Here|'s| a summary of the |2023 Nobel Prize laure|ates:

### |🧬| Physiology or Medicine
**|Katal|in Karikó and| Drew| We|issman**|
Awarded| for discoveries| enabling| the| development of effective| **|m|RNA vaccines**,| particularly| crucial| during| the COVID-19 pandemic.|

### |⚛|️ Physics|
**Pierre| Agost|ini,| Ferenc| Krausz, and Anne| L'Huillier**|
Recognized| for experimental| methods| generating| **att|osecond pulses of| light** to| study electron| dynamics||
"""
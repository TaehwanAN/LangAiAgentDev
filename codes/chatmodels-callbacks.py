"""
LangChain Callback Examples
Demonstrates three common callback use cases:
  1. Event Logging   — track LLM lifecycle events with timestamps
  2. Token Monitor   — count and report token usage
  3. Streaming UI    — print tokens in real-time as they arrive
"""

import time
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler

load_dotenv()


# ──────────────────────────────────────────────
# 1. Event Logging Callback
# ──────────────────────────────────────────────
class LoggingCallbackHandler(BaseCallbackHandler):
    """Logs each LLM lifecycle event with a timestamp."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LOG {_ts()}] LLM started  | prompt: '{prompts[0][:60]}...'")

    def on_llm_end(self, response, **kwargs):
        print(f"[LOG {_ts()}] LLM finished | generations: {len(response.generations)}")

    def on_llm_error(self, error, **kwargs):
        print(f"[LOG {_ts()}] LLM error    | {error}")


# ──────────────────────────────────────────────
# 2. Token Monitor Callback
# ──────────────────────────────────────────────
class TokenMonitorCallbackHandler(BaseCallbackHandler):
    """Counts streamed tokens and reports usage on completion."""

    def __init__(self):
        self.token_count = 0
        self.start_time = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.token_count = 0
        self.start_time = time.time()
        print("[TOKEN] Monitoring started...")

    def on_llm_new_token(self, token, **kwargs):
        self.token_count += 1

    def on_llm_end(self, response, **kwargs):
        elapsed = time.time() - self.start_time
        # API-reported usage (from response metadata when available)
        usage = response.llm_output.get("usage", {}) if response.llm_output else {}
        print(f"[TOKEN] Streamed tokens : {self.token_count}")
        print(f"[TOKEN] API usage       : {usage if usage else 'N/A (non-streaming)'}")
        print(f"[TOKEN] Elapsed time    : {elapsed:.2f}s")


# ──────────────────────────────────────────────
# 3. Streaming UI Callback
# ──────────────────────────────────────────────
class StreamingUICallbackHandler(BaseCallbackHandler):
    """Prints each token immediately to simulate a streaming chat UI."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("[UI] Assistant: ", end="", flush=True)

    def on_llm_new_token(self, token, **kwargs):
        print(token, end="", flush=True)

    def on_llm_end(self, response, **kwargs):
        print("\n[UI] Stream complete.")


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def _ts():
    return time.strftime("%H:%M:%S")


PROMPT = "Briefly explain what a neural network is in 2 sentences."

# ──────────────────────────────────────────────
# Demo 1: Event Logging (non-streaming)
# ──────────────────────────────────────────────
print("=" * 50)
print("Demo 1: Event Logging")
print("=" * 50)
model_log = ChatAnthropic(model='claude-haiku-4-5', callbacks=[LoggingCallbackHandler()])
response = model_log.invoke(PROMPT)
print(response.content)

# ──────────────────────────────────────────────
# Demo 2: Token Monitoring (streaming)
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("Demo 2: Token Monitoring")
print("=" * 50)
model_token = ChatAnthropic(model='claude-haiku-4-5', streaming=True, callbacks=[TokenMonitorCallbackHandler()])
response = model_token.invoke(PROMPT)
print(response.content)

# ──────────────────────────────────────────────
# Demo 3: Streaming UI
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("Demo 3: Streaming UI")
print("=" * 50)
model_stream = ChatAnthropic(model='claude-haiku-4-5', streaming=True, callbacks=[StreamingUICallbackHandler()])
model_stream.invoke(PROMPT)

"""
LangChain PostgreSQL Caching Example

Setup:
  1. Add to .env:
       DB_USER=postgres
       DB_PASSWORD=yourpassword
       DB_HOST=localhost
       DB_PORT=5432
       DB_NAME=postgres

  2. LangChain will auto-create the 'langchain_cache' table on first run.

How it works:
  - set_llm_cache(SQLAlchemyCache(engine)) registers a global cache backed by Postgres
  - Identical prompts + model params → cache hit (no API call)
  - Cache persists across process restarts (unlike InMemoryCache)
"""

import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine

from langchain_anthropic import ChatAnthropic
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLAlchemyCache

load_dotenv()

# ── DB connection ──────────────────────────────────────────
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "postgres")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# ── Register Postgres cache (creates table if not exists) ──
set_llm_cache(SQLAlchemyCache(engine))

# ── Model & prompt ─────────────────────────────────────────
model = ChatAnthropic(model='claude-haiku-4-5')
prompt = "Who is the president of North Korea?"

# ── 1st call: cache MISS → API call → result stored in DB ──
print("1st call (cache miss)...")
start = time.time()
response_1 = model.invoke(prompt)
print(f"  Time   : {time.time() - start:.3f}s")
print(f"  Answer : {response_1.content}\n")

# ── 2nd call: cache HIT → result returned from Postgres ────
print("2nd call (cache hit)...")
start = time.time()
response_2 = model.invoke(prompt)
print(f"  Time   : {time.time() - start:.3f}s")
print(f"  Answer : {response_2.content}\n")

# ── Verify cache hit ───────────────────────────────────────
print(f"Same response ID? {response_1.id == response_2.id}")  # True = cache hit

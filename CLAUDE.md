# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Udemy course project for learning LangChain and AI Agent development with Python.

## Environment Setup

- Python virtual environment: `.venv/` (Python 3.11.9)
- Activate: `source .venv/Scripts/activate` (Windows/bash)
- Install dependencies as needed: `pip install langchain-openai langchain`

## Running Code

```bash
python getting-started.py
```

No formal build system, test runner, or `requirements.txt` exists yet. Scripts are run directly.

## Architecture

- **Framework:** LangChain (`langchain_openai`, `langchain` packages)
- **Pattern:** Each script demonstrates a specific LangChain/agent concept
- **API Keys:** OpenAI API key required — set via environment variable `OPENAI_API_KEY` or pass directly (never commit real keys)
- **Model:** `ChatOpenAI` with GPT-4 backend is the baseline pattern

## Key Conventions

- One Python file per concept/lesson
- Scripts use `model.invoke(input=...)` for synchronous LLM calls and print `response.content`

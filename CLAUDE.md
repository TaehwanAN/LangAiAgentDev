# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Udemy course project for building LangChain AI agents with Python 3.11.

**Remote**: https://github.com/TaehwanAN/LangAiAgentDev

## Environment Setup

Virtual environment is at `.venv/`. Always activate before running scripts:

```bash
source .venv/Scripts/activate   # Windows/bash
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Key packages: `langchain`, `langchain-openai`, `langchain-anthropic`, `langchain-core`, `python-dotenv`.

## Running Scripts

```bash
python codes/chatmodels-setup.py
python codes/chatmodels-req-message.py
python codes/chatmodels-req-prompt.py
python codes/chatmodels-res-batch.py
```

API keys are loaded from `.env` via `python-dotenv`. The `.env` file must define `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`.

## Architecture

Scripts are standalone Python files under `codes/`. Each file demonstrates a specific LangChain concept from the course. The primary pattern is:

1. `load_dotenv()` to load API keys
2. Instantiate a model (`ChatOpenAI`, `ChatAnthropic`, etc.)
3. Invoke with a prompt string, message list, or `PromptTemplate`/`ChatPromptTemplate`
4. Print or process `response.content`

**Invocation methods demonstrated:**
- `model.invoke(prompt)` — single synchronous call
- `model.batch([prompt1, prompt2, ...])` — parallel batch calls
- `PromptTemplate.from_template(...)` — string prompt templating
- `ChatPromptTemplate(messages)` — structured system/user message templates
- `SystemMessage` / `HumanMessage` from `langchain_core.messages` — explicit message types

`knowledge_docs/` contains reference text files (sample responses, error examples) used for learning.

## Git Conventions

- Conventional commits: `feat:`, `chore:`, `fix:`
- `gh` CLI is not installed — use `git push` directly

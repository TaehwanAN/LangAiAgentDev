# LangChain Agent 구조와 작동 원리 분석

> `building-agent-single.py` — 개인 재무 어시스턴트 Agent 코드 해설

---

## 1. 개요 (Overview)

이 파일은 **LangChain Agent**를 활용해 개인 재무 어시스턴트를 구현한 예제입니다.
사용자는 자연어로 계좌 잔액 조회, 거래 내역 확인, 예산 계산, 계좌 이체를 요청할 수 있으며, Agent가 적절한 도구(Tool)를 선택하고 실행한 뒤 구조화된 응답을 반환합니다.

### LangChain Agent란?

**Agent**는 LLM(Large Language Model)이 단순히 텍스트를 생성하는 데 그치지 않고, **외부 도구를 사용해 실제 행동(Action)을 취할 수 있도록** 확장한 구조입니다.

```
일반 LLM:  사용자 입력 → LLM → 텍스트 출력
LangChain Agent: 사용자 입력 → LLM → 도구 선택 & 실행 → 결과 반영 → 최종 답변
```

---

## 2. 아키텍처 — 6가지 핵심 구성 요소

```
┌──────────────────────────────────────────────────────┐
│                   create_agent()                     │
│                                                      │
│  ┌─────────┐  ┌───────┐  ┌────────────────────────┐ │
│  │  Model  │  │ Tools │  │    Context Schema       │ │
│  │ (LLM)   │  │ (@tool│  │   (UserContext)         │ │
│  └─────────┘  └───────┘  └────────────────────────┘ │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Middleware │  │   Response   │  │ Checkpointer│  │
│  │ (3종류)    │  │   Format     │  │ (Memory)    │  │
│  └────────────┘  └──────────────┘  └─────────────┘  │
└──────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 코드 위치 |
|-----------|------|-----------|
| **Model** | 추론 엔진 (GPT-4o, GPT-4o-mini) | `init_chat_model()` L27–40 |
| **Tools** | Agent가 호출할 수 있는 함수들 | `@tool` 데코레이터 L122–272 |
| **Context Schema** | 사용자별 런타임 데이터 | `UserContext` dataclass L42–47 |
| **Middleware** | 모델/프롬프트/도구 실행 전후 처리 | L278–378 |
| **Structured Output** | 응답을 Pydantic 모델로 강제 구조화 | `ToolStrategy(FinancialResponse)` |
| **Checkpointer** | 멀티턴 대화 메모리 | `InMemorySaver()` L398 |

---

## 3. Model — LLM 초기화

```python
# L27–40
basic_model   = init_chat_model("gpt-4o-mini", temperature=0.5, max_tokens=512)
premium_model = init_chat_model("gpt-4o", max_tokens=2048)
platinum_model = init_chat_model("gpt-4o")
```

`init_chat_model()`은 모델 ID와 파라미터를 받아 LangChain 호환 Chat Model 객체를 반환합니다.
이 예제에서는 멤버십 등급에 따라 **다른 모델을 동적으로 선택**합니다 (Middleware에서 처리).

---

## 4. Tools — Agent의 행동 도구

### 4-1. `@tool` 데코레이터

`@tool`은 일반 Python 함수를 Agent가 호출 가능한 도구로 변환합니다.
**docstring**이 LLM에게 "이 도구가 무엇을 하는지"를 알려주는 설명서 역할을 합니다.

```python
# L122–147
@tool
def get_account_balance(
    account_type: str,
    runtime: ToolRuntime[UserContext]  # ← 사용자 컨텍스트 자동 주입
) -> str:
    """
    Get the current balance for a specific account for a user

    Args:
        account_type: Type of account - 'checking', 'savings', or 'investment'
    """
    user_id = runtime.context.user_id      # UserContext에서 user_id 접근
    currency = runtime.context.preferred_currency
    ...
```

### 4-2. ToolRuntime[UserContext] — 컨텍스트 주입

`ToolRuntime[T]`는 Tool이 실행될 때 Agent가 자동으로 주입해주는 특수 파라미터입니다.
LLM이 도구를 호출할 때 `runtime` 인수를 명시하지 않아도 되며, 사용자가 누구인지를 각 도구 내부에서 알 수 있게 됩니다.

```
LLM → "get_account_balance('checking')" 호출
Agent → runtime.context = alice_context 자동 주입
Tool → alice의 잔액 반환
```

### 4-3. 5개 도구 요약

| 도구 | 기능 | 컨텍스트 사용 |
|------|------|--------------|
| `get_account_balance` | 계좌 잔액 조회 + 통화 변환 | user_id, preferred_currency |
| `get_recent_transactions` | 최근 거래 내역 조회 | user_id |
| `calculate_budget` | 월 소득 대비 카테고리별 예산 계산 | 없음 (일반 계산) |
| `get_personalized_greeting` | 멤버십 등급별 맞춤 인사 | user_name, membership_tier |
| `transfer_money` | 계좌 간 이체 (유효성 검사 포함) | user_id |

---

## 5. Context Schema — 사용자별 데이터 주입

```python
# L42–47
@dataclass
class UserContext:
    user_id: str
    user_name: str
    membership_tier: str  # 'basic', 'premium', 'platinum'
    preferred_currency: str
```

Agent를 호출할 때 `context=` 파라미터로 전달합니다:

```python
# L444–449, L492–494
alice_context = UserContext(
    user_id="user_001",
    user_name="Alice Johnson",
    membership_tier="platinum",
    preferred_currency="USD"
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "잔액을 알려줘"}]},
    context=alice_context  # ← 여기서 주입
)
```

이 컨텍스트는 **Middleware와 Tools 모두에서** `runtime.context`로 접근 가능합니다.

---

## 6. Middleware — 실행 파이프라인 가로채기

Middleware는 Agent의 핵심 실행 흐름(모델 호출, 프롬프트 생성, 도구 실행) 전후에
**커스텀 로직을 삽입**하는 메커니즘입니다.

```
[사용자 입력]
      ↓
 dynamic_model_selector  (@wrap_model_call)   ← 모델 선택
      ↓
 tier_based_prompt       (@dynamic_prompt)    ← 프롬프트 생성
      ↓
     [LLM 추론]
      ↓
 handle_tool_errors      (@wrap_tool_call)    ← 도구 실행 & 에러 처리
      ↓
 [최종 응답]
```

### 6-1. `@wrap_model_call` — 모델 동적 선택

```python
# L278–297
@wrap_model_call
def dynamic_model_selector(request: ModelRequest, handler) -> ModelResponse:
    tier = request.runtime.context.membership_tier

    if tier == "platinum":
        request.override(model=platinum_model)   # gpt-4o (무제한)
    elif tier == "premium":
        request.override(model=premium_model)    # gpt-4o (2048 tokens)
    else:
        request.override(model=basic_model)      # gpt-4o-mini (512 tokens)

    return handler(request)  # 다음 단계로 전달
```

멤버십 등급에 따라 더 강력한(혹은 더 저렴한) 모델을 사용하도록 **매 호출 시** 동적으로 결정합니다.

### 6-2. `@dynamic_prompt` — 프롬프트 동적 생성

```python
# L299–342
@dynamic_prompt
def tier_based_prompt(request: ModelRequest) -> str:
    tier = request.runtime.context.membership_tier
    user_name = request.runtime.context.user_name

    base_prompt = f"You are a personal finance assistant helping {user_name}..."

    if tier == "platinum":
        return base_prompt + "...Provide detailed, comprehensive financial analysis..."
    elif tier == "premium":
        return base_prompt + "...Provide helpful explanations..."
    else:
        return base_prompt + "...Be concise and direct..."
```

고정된 `system_prompt` 대신, 사용자 등급에 맞는 **시스템 프롬프트를 런타임에 생성**합니다.

### 6-3. `@wrap_tool_call` — 도구 에러 핸들링

```python
# L344–378
@wrap_tool_call
def handle_tool_errors(request: ToolCallRequest, handler) -> ToolMessage:
    try:
        return handler(request)          # 도구 실행 시도
    except ValueError as e:
        return ToolMessage(              # 에러를 메시지로 변환 (Agent가 이해할 수 있게)
            content=f"⚠️ {tool_name} failed: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )
```

도구 실행 중 발생한 예외를 잡아 **ToolMessage로 변환**합니다.
Agent는 이 에러 메시지를 받고 다음 행동을 결정합니다 (재시도, 다른 방법 시도, 사용자에게 알림 등).

---

## 7. Agent 작동 원리 — ReAct Loop

LangChain Agent는 **ReAct (Reasoning + Acting)** 패턴으로 동작합니다.

```
┌─────────────────────────────────────────────────────┐
│                    ReAct Loop                        │
│                                                      │
│  [사용자 입력]                                        │
│       ↓                                              │
│  [THINK] LLM이 어떤 도구를 써야 할지 판단             │
│       ↓                                              │
│  [ACT]   도구 호출 요청 (tool_calls 생성)             │
│       ↓                                              │
│  [OBSERVE] 도구 실행 결과를 메시지로 받음              │
│       ↓                                              │
│  [THINK] 결과를 바탕으로 다음 행동 판단               │
│       ↓                                              │
│  도구가 더 필요하면 → [ACT] 반복                      │
│  충분한 정보가 모였으면 → [ANSWER] 최종 응답 생성      │
└─────────────────────────────────────────────────────┘
```

### 구체적인 실행 흐름 예시

**사용자**: "내 모든 계좌 잔액을 알려줘"

```
1. THINK: "checking, savings, investment 세 계좌를 모두 조회해야 한다"
2. ACT:   get_account_balance("checking") 호출
3. OBSERVE: "Your checking account balance is $2,500.00"
4. ACT:   get_account_balance("savings") 호출
5. OBSERVE: "Your savings account balance is $15,000.00"
6. ACT:   get_account_balance("investment") 호출
7. OBSERVE: "Your investment account balance is $45,000.00"
8. ANSWER: "당신의 계좌 현황입니다: 체킹 $2,500, 저축 $15,000, 투자 $45,000..."
```

---

## 8. `create_agent()` — Agent 조립

```python
# L400–418
agent = create_agent(
    model=basic_model,              # 기본 모델 (Middleware가 동적으로 변경)
    tools=[                         # 사용 가능한 도구 목록
        get_account_balance,
        get_recent_transactions,
        calculate_budget,
        get_personalized_greeting,
        transfer_money
    ],
    context_schema=UserContext,     # 런타임 컨텍스트 타입 지정
    middleware=[                    # 실행 파이프라인 커스터마이징
        dynamic_model_selector,
        tier_based_prompt,
        handle_tool_errors,
    ],
    response_format=ToolStrategy(FinancialResponse),  # 구조화된 응답 형식
    checkpointer=checkpointer       # 멀티턴 메모리
)
```

각 파라미터의 역할:

| 파라미터 | 타입 | 역할 |
|----------|------|------|
| `model` | ChatModel | Agent의 기본 추론 엔진 |
| `tools` | list | Agent가 사용할 수 있는 도구 목록 |
| `context_schema` | dataclass | 런타임 컨텍스트의 타입 정의 |
| `middleware` | list | 실행 전후 처리 함수들 |
| `response_format` | ToolStrategy | 최종 응답의 구조 (Pydantic 모델) |
| `checkpointer` | Checkpointer | 대화 히스토리 저장소 |

---

## 9. Structured Response — 구조화된 응답

```python
# L49–67
class FinancialResponse(BaseModel):
    summary: str          # 1–2문장 요약
    details: str          # 상세 설명
    action_items: list[str]  # 권장 행동 목록
    warnings: list[str]      # 경고/주의사항
    confidence: Literal["high", "medium", "low"]  # 신뢰도
```

`ToolStrategy(FinancialResponse)`를 `response_format`으로 지정하면,
Agent의 최종 응답이 이 Pydantic 모델 형태로 강제됩니다.

```python
# L537
response = agent.invoke(...)
structured: FinancialResponse = response["structured_response"]

print(structured.summary)        # "당신의 투자 계좌가 가장 많습니다..."
print(structured.action_items)   # ["저축 계좌 비중을 늘리세요", ...]
print(structured.confidence)     # "high"
```

---

## 10. Memory — 멀티턴 대화 기억

```python
# L398
checkpointer = InMemorySaver()

# Agent 호출 시 thread_id 지정
memory_config = {"configurable": {"thread_id": "alice-memory-test"}}

# Turn 1
response = agent.invoke(
    {"messages": [{"role": "user", "content": "내 계좌 잔액은?"}]},
    context=alice_context,
    config=memory_config   # ← 같은 thread_id로 대화 연결
)

# Turn 2 — 이전 대화 맥락 유지
response = agent.invoke(
    {"messages": [{"role": "user", "content": "어떤 계좌가 제일 많아?"}]},
    context=alice_context,
    config=memory_config   # ← 같은 thread_id
)
# Agent는 Turn 1의 잔액 조회 결과를 기억하고 있음
```

`thread_id`가 다르면 새로운 독립 대화 세션이 시작됩니다:

```
"alice-memory-test" → Alice의 대화 히스토리
"bob-002"           → Bob의 대화 히스토리 (완전히 별개)
```

---

## 11. Streaming — 실시간 응답

```python
# L604–617
for chunk in agent_for_streaming.stream(
    {"messages": [{"role": "user", "content": query}]},
    context=bob_context,
    config=bob_config,
    stream_mode="values"  # 매 상태 변화마다 전체 상태 전달
):
    latest_message = chunk['messages'][-1]

    if latest_message.content:
        print(f"Agent: {latest_message.content}")       # 텍스트 응답 청크
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
```

| stream_mode | 동작 |
|-------------|------|
| `"values"` | 매 단계마다 전체 메시지 상태를 반환 |
| `"updates"` | 매 단계마다 변경된 부분만 반환 |

`invoke()`는 최종 결과만 반환하지만, `stream()`은 Agent가 도구를 호출하는 중간 과정을
실시간으로 확인할 수 있어 **사용자 경험(UX) 개선**에 유용합니다.

---

## 12. 전체 실행 흐름 다이어그램

```
agent.invoke(messages, context=alice_context, config=memory_config)
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Middleware Pipeline                                         │
│                                                             │
│  1. dynamic_model_selector  → alice는 platinum → gpt-4o    │
│  2. tier_based_prompt       → platinum용 상세 분석 프롬프트  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │   LLM (gpt-4o)   │  ← 시스템 프롬프트 + 사용자 메시지 + 도구 목록
              │   THINK & PLAN   │
              └────────┬─────────┘
                       │ tool_calls 생성
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Tool Execution (handle_tool_errors Middleware 적용)         │
│                                                             │
│  get_account_balance("checking") → runtime.context=alice   │
│  get_account_balance("savings")  → runtime.context=alice   │
│  get_account_balance("investment")→ runtime.context=alice  │
└────────────────────────┬────────────────────────────────────┘
                         │ ToolMessage 결과들
                         ▼
              ┌──────────────────┐
              │   LLM (gpt-4o)   │  ← 도구 결과 + 이전 대화 (checkpointer)
              │   FINAL ANSWER   │
              └────────┬─────────┘
                       │
                       ▼
              FinancialResponse  ← ToolStrategy가 구조화
              {
                summary: "...",
                details: "...",
                action_items: [...],
                warnings: [...],
                confidence: "high"
              }
```

---

## 정리 — 핵심 개념 요약

| 개념 | 한 줄 설명 |
|------|-----------|
| **Agent** | LLM + Tools = 도구를 사용해 행동하는 AI |
| **ReAct Loop** | Think → Act → Observe를 반복하며 목표 달성 |
| **@tool** | 파이썬 함수를 LLM이 호출 가능한 도구로 변환 |
| **ToolRuntime** | 도구 실행 시 사용자 컨텍스트를 자동 주입 |
| **Middleware** | 모델/프롬프트/도구 실행을 가로채 커스터마이징 |
| **Checkpointer** | thread_id 기반 멀티턴 대화 메모리 |
| **ToolStrategy** | Pydantic 모델로 응답 구조를 강제 |
| **stream()** | 중간 과정(도구 호출 등)을 실시간으로 전달 |

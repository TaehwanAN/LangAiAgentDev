from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch

load_dotenv()

# 1. LLM Setup
model = ChatAnthropic(model = "claude-sonnet-4-6", temperature=0.8)

# --- Define Independent Runnables/Chains for Parallel Execution ---
# 2. Chain A: Generatres a concise sentence about a topic
sentence_prompt = ChatPromptTemplate.from_template(
  "Generate a one concise sentence about: {topic}"
)
sentence_chain = sentence_prompt | model | StrOutputParser()

# 3. Chain B: Generates a few keywords related to the same topic
keywords_prompt = ChatPromptTemplate.from_template(
  "List 3 to 5 comma-separated keywords related to the topic \"{topic}\". Do not add any extra text or intros."
)
keyword_chain = keywords_prompt | model | StrOutputParser()

# 4. Combine Chains in Parallel
parallel_chains = RunnableParallel(
  sentence=sentence_chain,keywords=keyword_chain
)

# --- Define Conditional Logic (Runnable Batch) ---
# 5. Custom RunnableLambda for the condition check
def is_sentence_short(data: dict) -> bool:
  """_summary_

  Args:
      data (dict): _description_

  Returns:
      bool: _description_
  """
  print(data)
  sentence = data.get("sentence","")
  print(f"\n--- DEBUG: Sentence Length Check ---")
  print(f"Sentence: '{sentence}' ({len(sentence)} length)")
  
  is_short = len(sentence) <= 50
  print(f"Is short sentence? {is_short}")
  return is_short  

sentence_length_checker = RunnableLambda(is_sentence_short)

# 6. Branch 1: Elaborate if the sentence is short
elaborate_prompt = ChatPromptTemplate.from_messages(
  [
    ("system","Elaborate on the following sentence using these keywords, adding more detail."),
    ("human", "Sentence: {sentence}\nKeywords: {keywords}\nElaboration:")
  ]
)
elaborate_chain = elaborate_prompt | model | StrOutputParser()

# 7. Branch 2: Summarize if the sentence is long
summarize_prompt = ChatPromptTemplate.from_messages(
  [
    ("system","Summarize the following sentence concisely into one shorter sentence, using these keywords to guide summary."),
    ("human", "Sentence: {sentence}\nKeywords: {keywords}\nSummary:") 
  ]
)
summarize_chain = summarize_prompt | model | StrOutputParser()

# 8. RunnableBranch: Directs flow based on the condition
conditional_branch = RunnableBranch(
  (sentence_length_checker, elaborate_chain), summarize_chain
)

# --- Assemble the Full Complex Chain ---
final_complex_chain = parallel_chains | conditional_branch
# print(final_complex_chain)

# --- Visualize the Complex Chain as ASCII Graph ---
chain_graph = final_complex_chain.get_graph()
chain_graph.print_ascii()

result = final_complex_chain.invoke(
  {"topic":"Mexican Political System"}
)

print(result)
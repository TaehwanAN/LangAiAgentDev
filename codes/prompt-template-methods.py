from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Who is the {role} of {country}")

# invoke()
invoked_prompt = prompt_template.invoke({
  "role": "President",
  "country":"Zimbabwe"
})
print(invoked_prompt)

# format()
formatted_prompt = prompt_template.format(role = "Prime Minister",country="UK")
print(formatted_prompt)

# batch()
batched_prompts = prompt_template.batch(
  [
    {"role":"Leader", "country":"China"},
    {"role":"the famous artist", "country":"South Korea"},
    {"role":"the leader of supreme court", "country":"Mexico"}
  ]
)
print(batched_prompts)

# Pretty Print()
prompt_template.pretty_print()

# save()
prompt_template.save("./examples/save_prompt_template.json")
prompt_template.save("./examples/save_prompt_template.yaml")
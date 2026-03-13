from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
  template = "Who is the {role} of {country}",
  input_types= {"country": str, "role": str},
  input_variables=["country","role"],
  optional_variables= ["gender"],
  validate_template=True
)

print(prompt_template.template)
print(prompt_template.template_format) # String or Jinja Template is also possible
print(prompt_template.input_variables)
print(prompt_template.input_types)
print(prompt_template.optional_variables)
print(prompt_template.validate_template)


# --- Jinja2 Template ---
jinja_template = PromptTemplate(
    template="Who is the {{ role }} of {{ country }}{% if year %} in {{ year }}{% endif %}?",
    template_format="jinja2"
)

print(jinja_template.template)
print(jinja_template.template_format)
print(jinja_template.input_variables)

# Format with all variables
print(jinja_template.format(role="president", country="USA", year="2024"))

# Format without optional variable ({% if %} skips the year clause when empty)
print(jinja_template.format(role="president", country="USA", year=""))
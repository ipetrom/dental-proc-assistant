from openai_utils import ask_openai 
from template_builder import get_descriptions_for_procedure, build_template_prompt, parse_fields_from_llm

#print(ask_openai("Hello, how are you?"))  

prompt = build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
fields_json_str = ask_openai(prompt)
#print(fields_json_str)

fields = parse_fields_from_llm(fields_json_str)
print(fields)


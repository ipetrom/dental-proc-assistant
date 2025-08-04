from openai_utils import ask_openai 
from template_builder import get_descriptions_for_procedure, build_template_prompt, parse_fields_from_llm, prepare_template_context, build_natural_text_prompt

#print(ask_openai("Hello, how are you?"))  

prompt = build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
fields_json_str = ask_openai(prompt)
#print(fields_json_str)

fields = parse_fields_from_llm(fields_json_str)
#print(fields)
natural_text_prompt = build_natural_text_prompt(fields)
print(natural_text_prompt)

#template_context = prepare_template_context(fields)
#print(template_context)
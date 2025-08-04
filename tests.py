from openai_utils import ask_openai 
from template_builder import get_descriptions_for_procedure, build_template_prompt, parse_fields_from_llm, prepare_template_context, build_story_template_prompt, extract_placeholders_from_template, tokenize_template

#print(ask_openai("Hello, how are you?"))  

prompt = build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
fields_json_str = ask_openai(prompt)
#print(fields_json_str)

fields = parse_fields_from_llm(fields_json_str)
#print(fields)
#natural_text_prompt = build_natural_text_prompt(fields)
#print(natural_text_prompt)

template_context = prepare_template_context(fields)
#print(template_context)

story_prompt = build_story_template_prompt(fields)
#print(story_prompt)

story_template_str = ask_openai(story_prompt)
#print(story_template_str)

placeholders = extract_placeholders_from_template(story_template_str)
#print(placeholders)

tokens = tokenize_template(story_template_str)
#print(tokens)
from openai_utils import ask_openai 
from template_builder import build_template_prompt2, get_descriptions_for_procedure, build_template_prompt, parse_fields_from_llm, build_story_template_prompt, extract_placeholders_from_template, tokenize_template, build_template_prompt2, parse_fields_from_llm2

#print(ask_openai("Hello, how are you?"))  

prompt = build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
fields_json_str = ask_openai(prompt)
#print(fields_json_str)

prompt2 = build_template_prompt2(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
fields_json_str2 = ask_openai(prompt2)
#print(fields_json_str2)

fields = parse_fields_from_llm(fields_json_str)
#print(fields)
#natural_text_prompt = build_natural_text_prompt(fields)
#print(natural_text_prompt)

fields2 = parse_fields_from_llm2(fields_json_str2)
#print(fields2)

#template_context = prepare_template_context(fields)
#print(template_context)

story_prompt = build_story_template_prompt(fields)
#print(story_prompt)

story_prompt2 = build_story_template_prompt(fields2)
#print(story_prompt2)

story_template_str = ask_openai(story_prompt)
#print(story_template_str)

story_template_str2 = ask_openai(story_prompt2)
#print(story_template_str2)

placeholders = extract_placeholders_from_template(story_template_str)
#print(placeholders)

placeholders2 = extract_placeholders_from_template(story_template_str2)
#print(placeholders2)

tokens = tokenize_template(story_template_str)
#print(tokens)

tokens2 = tokenize_template(story_template_str2)
#print(tokens2)

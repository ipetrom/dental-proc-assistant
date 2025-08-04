from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from template_builder import (
    get_descriptions_for_procedure,
    build_template_prompt,
    parse_fields_from_llm,
    build_story_template_prompt,
    extract_placeholders_from_template,
    tokenize_template
)
from openai_utils import ask_openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/procedure_story/{procedure_id}")
async def procedure_template(request: Request, procedure_id: str):

    # 1. Pobierz opisy
    descriptions = get_descriptions_for_procedure(procedure_id)
    if not descriptions:
        return {"error": "Brak opisów dla tej procedury."}
    
    # 2. Wygeneruj listę pól
    fields_prompt = build_template_prompt(descriptions)
    fields_json_str = ask_openai(fields_prompt)
    fields = parse_fields_from_llm(fields_json_str)    

    # 3. Wygeneruj naturalny szablon-opowieść z placeholderami
    story_prompt = build_story_template_prompt(fields)
    story_template_str = ask_openai(story_prompt)

    # 4. Podziel szablon na tokeny
    tokens = tokenize_template(story_template_str)

     # 5. Przygotuj mapę opcji dla każdego placeholdera
    fields_map = {f["field"]: f["options"] for f in fields}
 
    # 6. Przekaż dane do template
    context = {
        "request": request,
        "tokens": tokens,
        "fields_map": fields_map,
        "procedure_id": procedure_id
    }

    # 7. Renderuj szablon
    return templates.TemplateResponse("dynamic_template.html", context)
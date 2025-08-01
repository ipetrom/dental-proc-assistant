from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from template_builder import (
    get_descriptions_for_procedure,
    build_template_prompt,
    parse_fields_from_llm,
    prepare_template_context,
)
from openai_utils import ask_openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/procedure/{procedure_id}")
async def procedure_template(request: Request, procedure_id: str):
    # 1. Pobierz opisy
    descriptions = get_descriptions_for_procedure(procedure_id)
    if not descriptions:
        return {"error": "Brak opisów dla tej procedury."}
    # 2. Buduj prompt
    prompt = build_template_prompt(descriptions)
    # 3. Wyślij do OpenAI
    llm_response = ask_openai(prompt)
    # 4. Sparsuj JSON
    fields = parse_fields_from_llm(llm_response)
    # 5. Przygotuj kontekst do template
    context = prepare_template_context(fields)
    context["request"] = request  # wymagane przez Jinja2Templates
    context["procedure_id"] = procedure_id
    # 6. Renderuj szablon
    return templates.TemplateResponse("dynamic_template.html", context)

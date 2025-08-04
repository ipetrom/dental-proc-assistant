import json

def get_descriptions_for_procedure(procedure_id: str, json_path: str = "descriptions.json") -> list:
    """
    Zwraca listę opisów dla danej procedury na podstawie procedure_id.

    Args:
        procedure_id (str): Identyfikator procedury (np. 'filling_small')
        json_path (str): Ścieżka do pliku JSON z opisami

    Returns:
        list: Lista opisów (str) dla wybranej procedury. Jeśli brak, zwraca pustą listę.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for proc in data:
        if proc.get("procedure_id") == procedure_id:
            return proc.get("descriptions", [])
    return []


#print(get_descriptions_for_procedure("wypelnienie_jednopowierzchniowe", "descriptions.json"))

def build_template_prompt(descriptions: list[str]) -> str:
    """
    Buduje prompt dla LLM, na podstawie listy opisów procedur.

    Args:
        descriptions (list[str]): Lista opisów danej procedury

    Returns:
        str: Gotowy prompt do wysłania do LLM (OpenAI)
    """
    prompt = (
        "You are a helpful assistant for dental procedures. Based on the following descriptions of a dental procedure, generate a form template with fields to be filled in by the dentist after performing the procedure.\n"
        "For each field, suggest the ONLY 3 most common values and include an 'Other' option.\n\n"
        "Descriptions:\n"
    )
    for idx, desc in enumerate(descriptions, 1):
        prompt += f"{idx}. {desc}\n"
    prompt += (
        "\nReturn the response in JSON format:\n"
        "[\n"
        "  {\"field\": \"Powierzchnia\", \"options\": [\"okluzyjna\", \"mezjalna\", \"dystalna\", \"Other\"]},\n"
        "  ...\n"
        "]"\
        "\nTemplate should be user-friendly and easy to fill out, including emojis. In addition, make the template as human-like as possible\n"
    )
    return prompt

#print(build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json")))

def parse_fields_from_llm(llm_response: str) -> list[dict]:
    """
    Parsuje odpowiedź LLM (string w formacie JSON) na listę słowników.

    Args:
        llm_response (str): Odpowiedź z LLM, oczekiwana w formacie JSON

    Returns:
        list[dict]: Lista pól i opcji do template

    Raises:
        ValueError: Jeśli nie uda się sparsować JSONa
    """
    try:
        # Często LLM zwraca trochę zbędnych znaków, więc najpierw oczyszczamy
        llm_response = llm_response.strip()
        # Usuń niepotrzebny kod bloków, jeśli jest (np. ```json ... ```)
        if llm_response.startswith("```json"):
            llm_response = llm_response[7:]
        if llm_response.endswith("```"):
            llm_response = llm_response[:-3]
        # Próbuj parsować JSON
        return json.loads(llm_response)
    except Exception as e:
        raise ValueError(f"Błąd parsowania odpowiedzi LLM jako JSON: {e}\nOdpowiedź:\n{llm_response}")

def prepare_template_context(fields: list[dict]) -> dict:
    """
    Przygotowuje kontekst do renderowania szablonu Jinja2.

    Args:
        fields (list[dict]): Lista pól z opcjami (wynik z LLM)

    Returns:
        dict: Kontekst do przekazania do template (np. {"fields": fields})
    """
    return {"fields": fields}

def build_natural_text_prompt(fields: list[dict]) -> str:
    """
    Buduje prompt dla LLM, aby na podstawie listy pól i opcji wygenerował przykładowy naturalny opis zabiegu,
    w którym zmienne fragmenty są łatwo zamienne (np. do późniejszego wyboru przez lekarza).

    Args:
        fields (list[dict]): Lista pól z opcjami

    Returns:
        str: Prompt do wysłania do LLM
    """
    example = (
        "Example format:\n"
        "Tooth 47 – class II MOD cavity, but the filling only covers M + O (distal part untouched). V3 ring system, two layers of conventional composite. Contact point and fissures anatomically restored.\n"
        "\n"
        "Generate a similar, natural and concise dental procedure summary in Polish, where each important information is clearly separated and replaceable by a doctor (for each of the following fields, use a bracket for the value, e.g. Tooth: [Tooth], Filling material: [Material], etc.)."
        "\n"
        "Make the style sound like a real medical record comment. Use the field names as context.\n\n"
        "Fields:\n"
    )
    for field in fields:
        name = field.get("field", "")
        example += f"- {name}: [{name}]\n"
    prompt = (
        "You are an assistant for a dental procedure documentation system.\n"
        "Using the following list of fields, generate an example of a full, natural and human-like procedure comment enhancing user-friendly features adding emojis, "
        "using placeholders for values (so it can be filled by a doctor). "
        "Keep the order logical for medical notes and use professional language.\n"
        + example
    )
    return prompt

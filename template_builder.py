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

def build_story_template_prompt(fields: list[dict]) -> str:
    """
    Buduje prompt dla LLM, żeby na podstawie listy pól i opcji wygenerował naturalny, 
    spójny opis procedury stomatologicznej z placeholderami w kwadratowych nawiasach.

    Args:
        fields (list[dict]): Lista słowników zawierających 'field' i 'options'

    Returns:
        str: Gotowy prompt do wysłania do LLM
    """
    prompt = (
        "You are an assistant for a dental documentation system.\n"
        "Generate a concise, natural, professional summary of a dental procedure in Polish.\n"
        "For each of the fields below, use a placeholder in square brackets, e.g. [Ząb], [Klasa ubytku], etc.\n"
        "Connect all information in a single, natural narrative (not a list), like a medical note.\n"
        "Use medical language and keep it short.\n"
        "Here are the fields and example options:\n\n"
    )
    for field in fields:
        name = field.get("field", "")
        options = [opt for opt in field.get("options", []) if opt.lower() != "other"]
        if options:
            options_preview = ", ".join(options[:3])
            prompt += f"- {name}: {options_preview}\n"
        else:
            prompt += f"- {name}\n"
    prompt += (
        "\nReturn ONLY the template sentence with placeholders in square brackets. "
        "Do NOT use bullet points. Example: 'Ząb [Ząb] – ubytek klasy [Klasa ubytku] obejmujący powierzchnię [Powierzchnia]...'\n"
    )
    return prompt

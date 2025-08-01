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
    Buduje szablon zapytania na podstawie opisów.

    Args:
        descriptions (list[str]): Lista opisów do uwzględnienia w szablonie

    Returns:
        str: Zbudowany szablon zapytania
    """
    prompt = "Oto opisy dla procedury:\n"
    for desc in descriptions:
        prompt += f"- {desc}\n"
    return prompt
import os
from openai import OpenAI
from dotenv import load_dotenv
from template_builder import get_descriptions_for_procedure, build_template_prompt


load_dotenv()  # Wczytuje zmienne środowiskowe z .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(prompt: str, model: str = "gpt-4o") -> str:
    """
    Wysyła prompt do OpenAI i zwraca odpowiedź modelu (string, najlepiej JSON).
    
    Args:
        prompt (str): Tekst promptu do modelu LLM
        model (str): Nazwa modelu OpenAI (domyślnie gpt-4o)

    Returns:
        str: Odpowiedź modelu (string, najlepiej w formacie JSON)
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

#print(ask_openai("Hello, how are you?"))  

#prompt = build_template_prompt(get_descriptions_for_procedure("wypelnienie_dwupowierzchniowe", "descriptions.json"))
#fields_json_str = ask_openai(prompt)
#print(fields_json_str)
import os
from openai import OpenAI
from dotenv import load_dotenv


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
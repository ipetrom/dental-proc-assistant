import streamlit as st
from template_builder import (
    get_descriptions_for_procedure,
    build_template_prompt,
    parse_fields_from_llm,
    build_story_template_prompt,
    extract_placeholders_from_template,
    tokenize_template
)
from openai_utils import ask_openai


# Przykładowe nazwy procedur i ich ID
PROCEDURES = {
    "Plomba mała (jednopowierzchniowa)": "wypelnienie_jednopowierzchniowe",
    "Plomba średnia (dwupowierzchniowa)": "wypelnienie_dwupowierzchniowe",
    "Plomba duża (wielopowierzchniowa)": "wypelnienie_wielopowierzchniowe"
}

# Inicjalizacja stanu aplikacji
if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    st.markdown(
        """
        <style>
        .main-title {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 2.5em;
            font-weight: 900;
            margin-top: 16px;
            margin-bottom: 24px;
            letter-spacing: -2px;
        }
        .greeting {
            font-size: 1.45em;
            font-weight: 700;
            margin-bottom: 7px;
            margin-top: 8px;
        }
        .helptext {
            font-size: 1.08em;
            margin-bottom: 2em;
            color: #E0E0E0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Główny nagłówek – jedna linia
    st.markdown(
        """<div class='main-title'>🦷 Asystent opisu zabiegów stomatologicznych</div>""",
        unsafe_allow_html=True
    )
    # Powitanie, oddalone od nagłówka
    st.markdown(
        """<div class='greeting'>Hej! Jaką procedurę przeprowadziłeś? 🪄</div>""",
        unsafe_allow_html=True
    )
    # Instrukcja
    st.markdown(
        """<div class='helptext'>Wybierz jedną z dostępnych opcji, a ja pomogę Ci z wygenerowaniem profesjonalnego opisu medycznego 👇</div>""",
        unsafe_allow_html=True
    )
    procedure_label = st.selectbox(
        "Wybierz typ procedury:",
        list(PROCEDURES.keys())
    )
    if st.button("Dalej"):
        st.session_state["procedure_id"] = PROCEDURES[procedure_label]
        st.session_state["step"] = 2
        st.experimental_rerun()

if st.session_state.get("step") == 2:
    st.title("🦷 Opis zabiegu")
    st.markdown("### Uzupełnij dane w opisie poniżej:")

    procedure_id = st.session_state["procedure_id"]

    # --- Ten blok wykonuj TYLKO jeśli nie masz jeszcze danych ---
    if "fields" not in st.session_state or "tokens" not in st.session_state or "fields_map" not in st.session_state:
        descriptions = get_descriptions_for_procedure(procedure_id)
        fields_prompt = build_template_prompt(descriptions)
        fields_json_str = ask_openai(fields_prompt)
        fields = parse_fields_from_llm(fields_json_str)

        story_prompt = build_story_template_prompt(fields)
        story_template_str = ask_openai(story_prompt)
        tokens = tokenize_template(story_template_str)
        fields_map = {f["field"]: f["options"] for f in fields}

        st.session_state["fields"] = fields
        st.session_state["tokens"] = tokens
        st.session_state["fields_map"] = fields_map

    tokens = st.session_state["tokens"]
    fields_map = st.session_state["fields_map"]

    user_inputs = {}

    for token in tokens:
        if token["type"] == "text":
            # Pogrubiona opowieść
            st.markdown(f"<span style='font-weight:bold; font-size:1.12em'>{token['value']}</span>", unsafe_allow_html=True)
        elif token["type"] == "placeholder":
            label = token["value"]
            # Szary, mniejszy opis
            st.markdown(f"<span style='color:#888; font-size:0.95em;'> Wybierz dla: {label}</span>", unsafe_allow_html=True)
            options = fields_map.get(label, [])
            select_options = options.copy()
            if "Other" not in select_options:
                select_options.append("Other")
            key_base = f"{label}_{tokens.index(token)}"
            selected_option = st.selectbox(
                "",  # pusty label – opisy są nad polem
                select_options,
                key=key_base
            )
            if selected_option == "Other":
                other_key = key_base + "_other"
                other_val = st.text_input(
                    f"Podaj własną wartość dla: {label}",
                    key=other_key
                )
                user_inputs[label] = other_val
            else:
                user_inputs[label] = selected_option

    if st.button("Zatwierdź opis"):
        st.session_state["user_inputs"] = user_inputs
        st.session_state["step"] = 3
        st.experimental_rerun()

if st.session_state.get("step") == 3:
    st.title("🦷 Gotowy opis zabiegu")
    st.markdown("#### Skopiuj poniższy opis i wklej do dokumentacji pacjenta:")

    tokens = st.session_state["tokens"]
    user_inputs = st.session_state["user_inputs"]

    # Składanie finalnego tekstu
    final_text_html = ""
    for token in tokens:
        if token["type"] == "text":
            final_text_html += token["value"]
        elif token["type"] == "placeholder":
            value = user_inputs.get(token["value"], "")
            final_text_html += f"<span style='font-weight:bold; color:#fff09c'>{value}</span>"

    st.markdown(
        f"""
        <div style='font-size:1.3em; background: #232326; border-radius: 18px; padding: 28px 30px 18px 30px; margin-bottom: 18px; font-family: "Inter", sans-serif; font-weight: 400;'>
            {final_text_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Wróć do początku"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["step"] = 1
        st.rerun()  
        
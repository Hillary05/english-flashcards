import streamlit as st
from database import add_word


st.title("➕ Ajouter un mot")

st.write("Ajoute un nouveau mot à ton vocabulaire.")


word = st.text_input("Mot en anglais *")

translation = st.text_input("Traduction en français *")

definition = st.text_area("Définition en anglais")

example = st.text_area("Exemple de phrase")

personal_example = st.text_area(
    "Ta propre phrase avec ce mot"
)

part_of_speech = st.selectbox(
    "Nature du mot",
    [
        "",
        "noun",
        "verb",
        "adjective",
        "adverb",
        "pronoun",
        "preposition",
        "conjunction",
        "other"
    ]
)


if st.button("💾 Ajouter le mot"):

    if not word or not translation:
        st.warning("Le mot et la traduction sont obligatoires.")

    else:
        add_word(
            word,
            translation,
            definition,
            example,
            personal_example,
            part_of_speech,
        )

        st.success(f"Le mot « {word} » a été ajouté !")
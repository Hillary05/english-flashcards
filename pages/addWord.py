import streamlit as st
from database import add_word


st.title("➕ Ajouter un mot")

st.write("Ajoute un nouveau mot à ton vocabulaire.")


    # ─────────────────────────────────────
    # Informations générales sur le mot
    # ─────────────────────────────────────

word = st.text_input("Mot en anglais *", key="word")

st.markdown("---")

st.subheader("📖 Sens du mot")

# Nombre de sens à ajouter
number_of_meanings = st.number_input(
    "Nombre de sens",
    min_value=1,
    max_value=5,
    value=1,
    step=1,
    key="number_of_meanings"
)   

meanings = []

for i in range(int(number_of_meanings)):

    st.markdown(f"### Sens {i + 1}")

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
        ],
        key=f"part_of_speech_{i}"
    )

    translation = st.text_input(
        "Traduction *",
        key=f"translation_{i}"
    )

    definition = st.text_area(
        "Définition",
        key=f"definition_{i}"
    )

    example = st.text_area(
        "Exemple de phrase",
        key=f"example_{i}"
    )

    personal_example = st.text_area(
        "Ta propre phrase",
        key=f"personal_example_{i}"
    )

    meanings.append({
        "translation": translation,
        "definition": definition,
        "example": example,
        "personal_example": personal_example,
        "part_of_speech": part_of_speech
    })

    st.markdown("---")


# ─────────────────────────────────────
# Enregistrement
# ─────────────────────────────────────

if st.button("💾 Ajouter le mot"):

    if not word:
        st.warning("Le mot anglais est obligatoire.")

    elif any(not meaning["translation"] for meaning in meanings):
        st.warning(
            "Chaque sens doit avoir une traduction."
        )

    else:

        add_word(
            word=word,
            meanings=meanings,
        )

        st.success(
            f"Le mot « {word} » a été ajouté avec "
            f"{len(meanings)} sens !"
        )

        # Réinitialiser uniquement les champs de ce formulaire 
        keys_to_reset = [ "word", "number_of_meanings" ]

        for i in range(5): 
            keys_to_reset.extend([ 
                f"part_of_speech_{i}",
                f"translation_{i}", 
                f"definition_{i}", 
                f"example_{i}", 
                f"personal_example_{i}" 
            ])

        for key in keys_to_reset: 
            if key in st.session_state: 
                del st.session_state[key]

    # Recharger la page st.rerun()
    st.rerun()
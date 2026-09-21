import streamlit as st
from database import get_all_words, get_words_with_meanings, search_words


st.title("📚 Mon vocabulaire")

st.write("Voici tous les mots que tu as enregistrés.")

search_term = st.text_input("🔍 Rechercher un mot", placeholder="Tape un mot...")

words = get_words_with_meanings(search_term)


if not words:
    st.info("Aucun mot trouvé.....")

else:
    for word in words:

        st.subheader(word["word"])

        for meaning in word["meanings"]:

            if meaning["part_of_speech"]:
                st.write(
                    f"**Nature :** {meaning['part_of_speech']}"
                )

            st.write(
                f"**{meaning['definition']}**"
            )

            with st.expander("▼ Voir les détails"):

                if meaning["translation"]:
                    st.write("**Traduction :**")
                    st.write(meaning["translation"])

                if meaning["example"]:
                    st.write("**Exemple :**")
                    st.write(f"_{meaning['example']}_")

                if meaning["personal_example"]:
                    st.write("**Ma phrase :**")
                    st.write(f"_{meaning['personal_example']}_")

        st.divider()
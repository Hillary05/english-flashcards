import streamlit as st
from database import get_all_words, search_words


st.title("📚 Mon vocabulaire")

st.write("Voici tous les mots que tu as enregistrés.")

search_term = st.text_input("🔍 Rechercher un mot", placeholder="Tape un mot...")

if search_term:
    words = search_words(search_term)
else:
    words = get_all_words()


if not words:
    st.info("Ton vocabulaire est encore vide.")

else:
    for word in words:

        st.subheader(word["word"])

        st.write(f"**{word['translation']}**")

        # Informations supplémentaires
        with st.expander("▼ Voir les détails"):

            if word["definition"]:
                st.write("**Définition :**")
                st.write(word["definition"])

            if word["example"]:
                st.write("**Exemple :**")
                st.write(f"_{word['example']}_")

            if word["personal_example"]:
                st.write("**Ma phrase :**")
                st.write(f"_{word['personal_example']}_")

            if word["part_of_speech"]:
                st.write(
                    f"**Nature :** {word['part_of_speech']}"
                )

        st.divider()
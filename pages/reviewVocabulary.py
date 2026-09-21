import streamlit as st
from database import get_words_to_review, update_review


st.title("🧠 Réviser")

words = get_words_to_review()


if not words:
    st.info("Tu n'as aucun mot à réviser aujourd'hui. Reviens demain pour continuer à apprendre !")

else:

    # Initialiser l'index de la carte
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0

    # Initialiser l'état de la carte
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False


    # Récupérer le mot actuel
    word = words[st.session_state.current_card]


    st.markdown("---")

    # Afficher le mot
    st.subheader(word["word"])

    st.write("🤔 Quelle est la traduction de ce mot ?")


    # Bouton pour révéler la réponse
    if not st.session_state.show_answer:

        if st.button("🔓 Révéler"):

            st.session_state.show_answer = True

            st.rerun()


    # Afficher la réponse
    else:

        st.success(word["translation"])

        if word["definition"]:
            st.write(f"**Définition :** {word['definition']}")

        if word["example"]:
            st.write(f"**Exemple :** _{word['example']}_")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✓ Je savais"):

                update_review(word["id"], True)

                st.session_state.current_card += 1
                st.session_state.show_answer = False

                if st.session_state.current_card >= len(words):
                    st.session_state.current_card = 0

                st.rerun()

        with col2:
            if st.button("✗ Je ne savais pas"):

                update_review(word["id"], False)

                st.session_state.current_card += 1
                st.session_state.show_answer = False

                if st.session_state.current_card >= len(words):
                    st.session_state.current_card = 0

                st.rerun()
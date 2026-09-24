import streamlit as st
from database import get_words_to_review, update_review


st.title("🧠 Réviser")

words = get_words_to_review()

# ─────────────────────────────────────
# Créer une carte pour chaque sens
# ─────────────────────────────────────

cards = []

for word in words:

    for meaning in word["meanings"]:

        cards.append({
            "word_id": word["id"],
            "word": word["word"],
            "level": word["level"],
            "meaning": meaning
        })


if not cards:
    st.info("Tu n'as aucun mot à réviser aujourd'hui. Reviens demain pour continuer à apprendre !")

else:

    # Initialiser l'index de la carte
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0

    # Initialiser l'état de la carte
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    # Mémoriser les résultats des sens du mot actuel
    if "current_word_results" not in st.session_state:
        st.session_state.current_word_results = []

    # Sécurité : éviter un index hors limites
    if st.session_state.current_card >= len(cards):
        st.session_state.current_card = 0


    # Récupérer la carte actuelle (mot et sens)
    card = cards[st.session_state.current_card]

    # Récupérer le mot
    word = card["word"]

    # Récupérer le / les sens du mot
    meaning = card["meaning"]

    # Progression de la session
    current_position = st.session_state.current_card + 1
    total_cards = len(cards)

    st.write(
        f"**Carte {current_position} / {total_cards}**"
    )

    progress = current_position / total_cards

    st.progress(progress)


    st.markdown("---")

    if not st.session_state.show_answer:

        # ─────────────────────────────────────
        # Face avant
        # ─────────────────────────────────────

        with st.container(border=True):

            st.markdown(
                f"<h1 style='text-align: center;'>{word}</h1>",
                unsafe_allow_html=True
            )

            st.divider()

            st.markdown(
                """
                <p style="
                    text-align: center;
                    font-size: 18px;
                ">
                    🤔 Quelle est la traduction de ce sens ?
                </p>
                """,
                unsafe_allow_html=True
            )

        if st.button(
            "🔓 Révéler",
            use_container_width=True
        ):

            st.session_state.show_answer = True
            st.rerun()


    else:

        # ─────────────────────────────────────
        # Face arrière
        # ─────────────────────────────────────
 
        part_of_speech = meaning["part_of_speech"] or ""
        translation = meaning["translation"] or ""
        definition = meaning["definition"] or ""
        example = meaning["example"] or ""
        personal_example = meaning["personal_example"] or ""

        # Carte
        with st.container(border=True):

            st.markdown(
                f"<h1 style='text-align: center;'>{word}</h1>",
                unsafe_allow_html=True
            )

            if part_of_speech:
                st.markdown(
                    f"<p style='text-align: center; font-style: italic;'>"
                    f"{part_of_speech}"
                    f"</p>",
                    unsafe_allow_html=True
                )

            st.divider()

            st.markdown(
                f"<h2 style='text-align: center;'>{translation}</h2>",
                unsafe_allow_html=True
            )

            if definition:
                st.markdown("**📖 Définition :**")
                st.write(definition)

            if example:
                st.markdown("**💬 Exemple :**")
                st.markdown(f"*{example}*")

            if personal_example:
                st.markdown("**✏️ Ma phrase :**")
                st.markdown(f"*{personal_example}*")

        # Vérifier si cette carte est le dernier sens du mot actuel
        is_last_meaning = (
            st.session_state.current_card == len(cards) - 1
            or cards[st.session_state.current_card + 1]["word_id"] != card["word_id"]
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✓ Je savais",
                use_container_width=True
            ):

                # Mémoriser la réponse pour ce sens
                st.session_state.current_word_results.append(True)

                # Si c'est le dernier sens du mot,
                # appliquer une seule fois la décision Leitner
                if is_last_meaning:

                    all_meanings_known = all(
                        st.session_state.current_word_results
                    )

                    update_review(
                        card["word_id"],
                        all_meanings_known
                    )

                    # Réinitialiser les résultats pour le prochain mot
                    st.session_state.current_word_results = []

                st.session_state.current_card += 1
                st.session_state.show_answer = False

                if st.session_state.current_card >= len(cards):
                    st.session_state.current_card = 0


                st.rerun()

        with col2:

            if st.button(
                "✗ Je ne savais pas",
                use_container_width=True
            ):

                # Mémoriser la réponse pour ce sens
                st.session_state.current_word_results.append(False)

                 # Si c'est le dernier sens du mot,
                # appliquer une seule fois la décision Leitner
                if is_last_meaning:

                    all_meanings_known = all(
                        st.session_state.current_word_results
                    )

                    update_review(
                        card["word_id"],
                        all_meanings_known
                    )

                    # Réinitialiser les résultats pour le prochain mot
                    st.session_state.current_word_results = []

                st.session_state.current_card += 1
                st.session_state.show_answer = False

                if st.session_state.current_card >= len(cards):
                    st.session_state.current_card = 0

                st.rerun()
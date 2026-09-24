import sqlite3

DATABASE_NAME = "flashcards.db"

def get_connection():
    """Create and return a connection to the SQLite database."""
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        connection.row_factory = sqlite3.Row
        return connection

    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion à la base : {e}")
        return None


def create_table(connection):
    """Create the words and meanings tables."""

    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level INTEGER DEFAULT 0,
                last_reviewed TIMESTAMP,
                next_review TIMESTAMP
            )
        ''')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meanings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            translation TEXT NOT NULL,
            definition TEXT,
            example TEXT,
            personal_example TEXT,
            part_of_speech TEXT,
            FOREIGN KEY (word_id) REFERENCES words(id)
        )
    """)

    connection.commit()

def add_word(word, meanings):
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Vérifier si le mot existe déjà
    cursor.execute("""
        SELECT id
        FROM words
        WHERE word = ?
    """, (word,))

    existing_word = cursor.fetchone()

    if existing_word:
        word_id = existing_word["id"]

    else:
        cursor.execute("""
            INSERT INTO words (word)
            VALUES (?)
        """, (word,))

        word_id = cursor.lastrowid

    # Ajouter chaque sens seulement s'il n'existe pas déjà
    for meaning in meanings:

        cursor.execute("""
            SELECT id
            FROM meanings
            WHERE word_id = ?
              AND translation = ?
              AND definition = ?
              AND example = ?
              AND personal_example = ?
              AND part_of_speech = ?
        """, (
            word_id,
            meaning["translation"],
            meaning.get("definition"),
            meaning.get("example"),
            meaning.get("personal_example"),
            meaning.get("part_of_speech")
        ))

        existing_meaning = cursor.fetchone()

        if existing_meaning:
            continue

        cursor.execute("""
            INSERT INTO meanings (
                word_id,
                translation,
                definition,
                example,
                personal_example,
                part_of_speech
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            word_id,
            meaning["translation"],
            meaning.get("definition"),
            meaning.get("example"),
            meaning.get("personal_example"),
            meaning.get("part_of_speech")
        ))

    connection.commit()
    connection.close()

def get_all_words():
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            words.id,
            words.word,
            words.date_added,
            words.level,
            words.last_reviewed,
            words.next_review,
            meanings.id AS meaning_id,
            meanings.translation,
            meanings.definition,
            meanings.example,
            meanings.personal_example,
            meanings.part_of_speech
        FROM words
        LEFT JOIN meanings
            ON words.id = meanings.word_id
        ORDER BY words.word
    """)

    words_rows = cursor.fetchall()

    connection.close()

    return words_rows

def update_review(word_id, knew_word):
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    if knew_word:
        # Récupérer le niveau actuel du mot
        cursor.execute("""
            SELECT level
            FROM words
            WHERE id = ?
        """, (word_id,))

        word = cursor.fetchone()

        if word:
            current_level = word["level"]

            # Monter d'une boîte, avec un maximum de 5
            new_level = min(current_level + 1, 5)

            # Déterminer le délai avant la prochaine révision
            intervals = {
                1: 1,
                2: 2,
                3: 4,
                4: 7,
                5: 14
            }

            days = intervals[new_level]
        
        cursor.execute("""
                UPDATE words
                SET level = ?,
                    last_reviewed = CURRENT_TIMESTAMP,
                    next_review = datetime(
                        'now',
                        '+' || ? || ' days'
                    )
                WHERE id = ?
            """, (new_level, days, word_id))
    
    else:
        # Une mauvaise réponse renvoie le mot dans la boîte 1
        cursor.execute("""
            UPDATE words
            SET level = 1,
                last_reviewed = CURRENT_TIMESTAMP,
                next_review = datetime(
                    'now',
                    '+1 day'
                )
            WHERE id = ?
        """, (word_id,))

    connection.commit()
    connection.close()

def search_words(search_term):
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            words.id,
            words.word,
            words.date_added,
            words.level,
            words.last_reviewed,
            words.next_review,
            meanings.id AS meaning_id,
            meanings.translation,
            meanings.definition,
            meanings.example,
            meanings.personal_example,
            meanings.part_of_speech
        FROM words
        LEFT JOIN meanings
            ON words.id = meanings.word_id
        WHERE words.word LIKE ?
           OR meanings.translation LIKE ?
           OR meanings.definition LIKE ?
        ORDER BY words.word
    """, (
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%"
    ))

    words_rows = cursor.fetchall()

    connection.close()

    return words_rows

def get_words_with_meanings(search_term=None):
    if search_term:
        rows = search_words(search_term)
    else:
        rows = get_all_words()

    words = {}

    for row in rows:

        word_id = row["id"]

        if word_id not in words:
            words[word_id] = {
                "id": row["id"],
                "word": row["word"],
                "date_added": row["date_added"],
                "level": row["level"],
                "last_reviewed": row["last_reviewed"],
                "next_review": row["next_review"],
                "meanings": []
            }

        if row["meaning_id"] is not None:
            words[word_id]["meanings"].append({
                "id": row["meaning_id"],
                "translation": row["translation"],
                "definition": row["definition"],
                "example": row["example"],
                "personal_example": row["personal_example"],
                "part_of_speech": row["part_of_speech"]
            })

    return list(words.values())

def get_words_to_review():
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            words.id,
            words.word,
            words.date_added,
            words.level,
            words.last_reviewed,
            words.next_review,
            meanings.id AS meaning_id,
            meanings.translation,
            meanings.definition,
            meanings.example,
            meanings.personal_example,
            meanings.part_of_speech
        FROM words
        LEFT JOIN meanings
            ON words.id = meanings.word_id
        WHERE words.next_review IS NULL
           OR words.next_review <= CURRENT_TIMESTAMP
        ORDER BY words.next_review
    """)

    rows = cursor.fetchall()

    connection.close()

    # Regrouper les différents sens
    words = {}

    for row in rows:

        word_id = row["id"]

        if word_id not in words:
            words[word_id] = {
                "id": row["id"],
                "word": row["word"],
                "date_added": row["date_added"],
                "level": row["level"],
                "last_reviewed": row["last_reviewed"],
                "next_review": row["next_review"],
                "meanings": []
            }

        if row["meaning_id"] is not None:
            words[word_id]["meanings"].append({
                "id": row["meaning_id"],
                "translation": row["translation"],
                "definition": row["definition"],
                "example": row["example"],
                "personal_example": row["personal_example"],
                "part_of_speech": row["part_of_speech"]
            })

    return list(words.values())

# def get_words_to_review():
#     connection = get_connection()

#     if connection is None:
#         return []

#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT *
#         FROM words
#         WHERE next_review IS NULL
#            OR next_review <= CURRENT_TIMESTAMP
#         ORDER BY next_review
#     """)

#     words = cursor.fetchall()

#     connection.close()

#     return words

def initialize_database():
    connection = get_connection()

    if connection:
        create_table(connection)
        connection.close()

initialize_database()
 

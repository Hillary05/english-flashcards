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
    """Create the words table in the SQLite database."""

    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                definition TEXT,
                example TEXT,
                personal_example TEXT,
                part_of_speech TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level INTEGER DEFAULT 0,
                last_reviewed TIMESTAMP,
                next_review TIMESTAMP
            )
        ''')

    connection.commit()

def add_word(
        word,
        translation,
        definition=None,
        example=None,
        personal_example=None,
        part_of_speech=None
    ):
    connection = get_connection()
    if connection is None:
        print("Erreur lors de la connexion à la base de données.")
        return
    
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO words (word, translation, definition, example, personal_example, part_of_speech)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (word, translation, definition, example, personal_example, part_of_speech))
    connection.commit()
    connection.close()

def get_all_words():
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM words")

    words = cursor.fetchall()

    connection.close()

    return words

def search_words(search_term):
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM words
        WHERE word LIKE ?
        ORDER BY word
    """, (f"%{search_term}%",))

    words = cursor.fetchall()

    connection.close()

    return words

def initialize_database():
    connection = get_connection()

    if connection:
        create_table(connection)
        connection.close()

initialize_database()
 

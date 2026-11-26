import sqlite3
import os

if os.environ.get("VERCEL"):
    import tempfile
    DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_db(db_path=None):
    target = db_path or DB_PATH
    conn = sqlite3.connect(target)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            exam TEXT NOT NULL CHECK(exam IN ('NEET','JEE')),
            class_level TEXT NOT NULL CHECK(class_level IN ('11','12')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS pyqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam TEXT NOT NULL,
            year INTEGER NOT NULL,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            question_text TEXT NOT NULL,
            source_url TEXT NOT NULL,
            pdf_file TEXT,
            is_pyq INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL CHECK(correct_option IN ('a','b','c','d')),
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            explanation TEXT,
            question_number INTEGER NOT NULL,
            FOREIGN KEY(test_id) REFERENCES tests(id)
        );

        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            test_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL DEFAULT 20,
            answers_json TEXT NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(test_id) REFERENCES tests(id)
        );

        CREATE TABLE IF NOT EXISTS weak_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            test_result_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            subject TEXT NOT NULL,
            wrong_count INTEGER NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(test_result_id) REFERENCES test_results(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()

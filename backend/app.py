import os
import json
import sqlite3
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from init_db import init_db

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_frontend_path():
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"),
        os.path.join(os.getcwd(), "frontend", "index.html"),
        os.path.join(os.path.dirname(__file__), "frontend", "index.html"),
        os.path.join(os.path.dirname(__file__), "index.html")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]

@app.route("/", methods=["GET"])
def index():
    return send_file(get_frontend_path())

@app.route("/api/pdf/<path:filename>", methods=["GET"])
def get_pdf(filename):
    candidates = [
        os.path.join(os.path.dirname(__file__), "static", "pdfs"),
        os.path.join(os.getcwd(), "backend", "static", "pdfs"),
        os.path.join(os.getcwd(), "static", "pdfs"),
    ]
    for base in candidates:
        filepath = os.path.join(base, filename)
        if os.path.exists(filepath):
            as_download = request.args.get("download", "0") == "1"
            return send_file(
                filepath,
                mimetype="application/pdf",
                as_attachment=as_download,
                download_name=filename
            )
    return jsonify({"error": "PDF not found"}), 404

if os.environ.get("VERCEL"):
    import shutil
    DB_PATH = "/tmp/database.db"
    orig_db = os.path.join(os.path.dirname(__file__), "database.db")
    if not os.path.exists(DB_PATH) and os.path.exists(orig_db):
        try:
            shutil.copy2(orig_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_app_database():
    init_db(DB_PATH)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        count = c.execute("SELECT COUNT(*) FROM tests").fetchone()[0]
        conn.close()
        if count == 0:
            from seed import seed
            seed(DB_PATH)
    except Exception as e:
        print(f"Auto-seed exception: {e}")

init_app_database()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─── LOGIN ────────────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    exam = (data.get("exam") or "").strip().upper()
    class_level = str(data.get("class_level") or "").strip()

    if not name:
        return jsonify({"error": "Name is required."}), 400
    if exam not in ("NEET", "JEE"):
        return jsonify({"error": "Exam must be NEET or JEE."}), 400
    if class_level not in ("11", "12"):
        return jsonify({"error": "Class must be 11 or 12."}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (name, exam, class_level) VALUES (?, ?, ?)",
        (name, exam, class_level),
    )
    conn.commit()
    student_id = c.lastrowid
    conn.close()

    return jsonify({
        "id": student_id,
        "name": name,
        "exam": exam,
        "class_level": class_level,
    }), 201


# ─── STUDENT ──────────────────────────────────────────────────────────────────

@app.route("/api/student/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found."}), 404
    return jsonify(dict(row))


# ─── PYQs ─────────────────────────────────────────────────────────────────────

@app.route("/api/pyqs", methods=["GET"])
def get_pyqs():
    exam = request.args.get("exam", "").upper()
    if exam not in ("NEET", "JEE"):
        return jsonify({"error": "Exam must be NEET or JEE."}), 400
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM pyqs WHERE exam = ? AND is_pyq = 1 ORDER BY year DESC, subject",
        (exam,),
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ─── TESTS ────────────────────────────────────────────────────────────────────

@app.route("/api/tests", methods=["GET"])
def get_tests():
    exam = request.args.get("exam", "").upper()
    if exam not in ("NEET", "JEE"):
        return jsonify({"error": "Exam must be NEET or JEE."}), 400
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tests WHERE exam = ?", (exam,)
    ).fetchall()
    result = []
    for r in rows:
        t = dict(r)
        # Count questions per subject
        subjects = conn.execute(
            "SELECT subject, COUNT(*) as cnt FROM questions WHERE test_id = ? GROUP BY subject",
            (t["id"],),
        ).fetchall()
        t["subject_breakdown"] = {s["subject"]: s["cnt"] for s in subjects}
        result.append(t)
    conn.close()
    return jsonify(result)


@app.route("/api/test/<int:test_id>", methods=["GET"])
def get_test(test_id):
    conn = get_db()
    test = conn.execute("SELECT * FROM tests WHERE id = ?", (test_id,)).fetchone()
    if not test:
        conn.close()
        return jsonify({"error": "Test not found."}), 404
    questions = conn.execute(
        "SELECT id, question_number, question_text, option_a, option_b, option_c, option_d, subject, topic "
        "FROM questions WHERE test_id = ? ORDER BY question_number",
        (test_id,),
    ).fetchall()
    conn.close()
    return jsonify({
        "test": dict(test),
        "questions": [dict(q) for q in questions],
    })


# ─── SUBMIT TEST ──────────────────────────────────────────────────────────────

@app.route("/api/submit_test", methods=["POST"])
def submit_test():
    data = request.get_json()
    student_id = data.get("student_id")
    test_id = data.get("test_id")
    answers = data.get("answers", {})  # {str(question_id): 'a'|'b'|'c'|'d'}

    if not student_id or not test_id:
        return jsonify({"error": "student_id and test_id are required."}), 400

    conn = get_db()

    # Verify student and test exist
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    questions = conn.execute(
        "SELECT * FROM questions WHERE test_id = ? ORDER BY question_number",
        (test_id,),
    ).fetchall()
    if not questions:
        conn.close()
        return jsonify({"error": "Test not found or has no questions."}), 404

    correct_list = []
    incorrect_list = []
    blank_list = []
    topic_wrong = {}  # topic -> {count, subject}

    for q in questions:
        qid = str(q["id"])
        selected = answers.get(qid, "").lower().strip()
        q_dict = dict(q)

        entry = {
            "id": q["id"],
            "question_number": q["question_number"],
            "question_text": q["question_text"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "correct_option": q["correct_option"],
            "explanation": q["explanation"],
            "subject": q["subject"],
            "topic": q["topic"],
            "selected": selected or None,
        }

        if not selected:
            blank_list.append(entry)
        elif selected == q["correct_option"]:
            correct_list.append(entry)
        else:
            incorrect_list.append(entry)
            key = q["topic"]
            if key not in topic_wrong:
                topic_wrong[key] = {"count": 0, "subject": q["subject"]}
            topic_wrong[key]["count"] += 1

    score = len(correct_list)
    total = 20

    # Weak topics: only if wrong_count > 2 (i.e., 3 or more wrong)
    weak_topics = [
        {"topic": t, "subject": v["subject"], "wrong_count": v["count"]}
        for t, v in topic_wrong.items()
        if v["count"] > 2
    ]

    answers_json = json.dumps(answers)
    c = conn.cursor()
    c.execute(
        "INSERT INTO test_results (student_id, test_id, score, total, answers_json) VALUES (?, ?, ?, ?, ?)",
        (student_id, test_id, score, total, answers_json),
    )
    result_id = c.lastrowid

    for wt in weak_topics:
        c.execute(
            "INSERT INTO weak_topics (student_id, test_result_id, topic, subject, wrong_count) VALUES (?,?,?,?,?)",
            (student_id, result_id, wt["topic"], wt["subject"], wt["wrong_count"]),
        )

    conn.commit()
    conn.close()

    return jsonify({
        "result_id": result_id,
        "score": score,
        "total": total,
        "correct": correct_list,
        "incorrect": incorrect_list,
        "blank": blank_list,
        "weak_topics": weak_topics,
    })


# ─── RESULTS ──────────────────────────────────────────────────────────────────

@app.route("/api/results/<int:student_id>", methods=["GET"])
def get_results(student_id):
    conn = get_db()
    rows = conn.execute(
        """SELECT tr.*, t.name as test_name, t.exam
           FROM test_results tr
           JOIN tests t ON tr.test_id = t.id
           WHERE tr.student_id = ?
           ORDER BY tr.completed_at DESC""",
        (student_id,),
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ─── DOUBT SOLVER ─────────────────────────────────────────────────────────────

@app.route("/api/doubt", methods=["POST"])
def doubt_solver():
    data = request.get_json()
    question = (data.get("question") or "").strip()
    student_id = data.get("student_id")

    if not question:
        return jsonify({"error": "Question is required."}), 400

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return jsonify({"error": "AI service is not configured. Please set GEMINI_API_KEY in Replit Secrets."}), 503

    system_prompt = (
        "You are StudyMate AI, a doubt solver for Class 11 and 12 students preparing for NEET and JEE. "
        "Only answer questions related to Physics, Chemistry, Biology (for NEET), and Mathematics (for JEE) "
        "at the Class 11-12 level. If asked about anything outside this scope, politely explain that you can "
        "only help with Class 11-12 NEET/JEE science and mathematics topics. "
        "Be concise, clear, and use step-by-step explanations when solving problems."
    )

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        candidate_models = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro",
        ]
        answer = None
        last_err = None

        for m_name in candidate_models:
            try:
                model = genai.GenerativeModel(
                    m_name,
                    system_instruction=system_prompt,
                )
                response = model.generate_content(question)
                if response and response.text:
                    answer = response.text
                    break
            except Exception as model_err:
                last_err = model_err
                print(f"Model {m_name} failed: {model_err}")
                continue

        if not answer:
            raise Exception(f"All candidate models failed. Last error: {str(last_err)}")

    except Exception as e:
        print(f"Doubt solver error: {e}")
        return jsonify({"error": f"AI service error: {str(e)}"}), 503

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

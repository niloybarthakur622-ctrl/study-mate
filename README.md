# StudyMate 📚

**Smart NEET & JEE Practice Platform for Class 11 & 12**

---

## What's Inside

| Layer | Tech |
|---|---|
| Frontend | Single-page HTML/CSS/JS (no framework) |
| Backend | Python Flask REST API |
| Database | SQLite (auto-created on first run) |
| AI | Google Gemini 1.5 Flash via `google-generativeai` |

---

## Project Structure

```
studymate/
├── backend/
│   ├── app.py          # Flask API server
│   ├── init_db.py      # Creates SQLite tables
│   ├── seed.py         # Populates DB with PYQs & practice tests
│   └── requirements.txt
└── frontend/
    └── index.html      # Full SPA (HTML + CSS + JS)
```

---

## Replit Setup (Step-by-Step)

### 1. Import the Project

Upload/drag the `studymate/` folder into a **new Replit project** (Python template works best).

Or create a new **Flask Repl** and paste the files manually.

---

### 2. Set the AI Secret Key

StudyMate uses the **Google Gemini API** for the Doubt Solver.

1. In Replit, open the **Secrets** tab (🔒 icon on the left sidebar).
2. Add a new secret:
   - **Key:** `AQ.Ab8RN6J3OIybYaJrY8HtX3xYNXnfYfkHz2v5yRXwVsj5tBpBjwAPI`
   - **Value:** Your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

> ⚠️ Never paste your API key directly in the code. Always use Replit Secrets.

---

### 3. Install Dependencies

In the Replit Shell, run:

```bash
cd backend
pip install -r requirements.txt
```

---

### 4. Set Up the Database

```bash
cd backend
python seed.py
```

This will:
- Create `backend/database.db` (SQLite)
- Create all tables (students, pyqs, tests, questions, test_results, weak_topics)
- Insert 20 PYQs (10 NEET + 10 JEE, years 2023 & 2024)
- Insert 6 practice tests (3 NEET + 3 JEE, 20 questions each)

> You can re-run `seed.py` at any time to reset the database.

---

### 5. Run the Backend

```bash
cd backend
python app.py
```

The Flask server starts on **port 5000**.

---

### 6. Open the Frontend

Open `frontend/index.html` in a browser.

If testing locally, make sure the backend is running at `http://localhost:5000`.

**On Replit:** 
- The backend URL will be your Repl's URL (e.g., `https://your-repl-name.repl.co`).
- Update the `API` constant in `frontend/index.html` (line near top of `<script>`) to match:

```js
const API = "https://your-repl-name.repl.co";
```

---

## Running Both Together (Replit `.replit` file)

Create a `.replit` file at the project root:

```toml
run = "cd backend && python app.py"
```

Then serve the frontend using Python's built-in server or Replit's static hosting.

---

## Features

### Login Screen
- Enter name, choose exam (NEET or JEE), choose class (11th or 12th)
- Validates all fields before submitting
- Saves student to database
- Remembers session in localStorage

### Home Screen
- Personalized welcome: "Welcome, [Name]! 👋"
- Three cards: PYQs, Practice Tests, Doubt Solver
- Content filtered to student's chosen exam

### PYQs
- 2024 and 2023 questions from NEET/JEE clearly labelled as PYQs
- Subject badge, topic, question text
- Link to official NTA source page
- "Ask Doubt" button opens Doubt Solver pre-filled with the topic

### Practice Tests
- 3 tests per exam, 20 questions each
- Clearly labelled as "Practice Tests" (not real exam papers)
- **NEET:** 10 Physics + 5 Chemistry + 5 Biology
- **JEE:** 10 Mathematics + 5 Chemistry + 5 Physics
- Progress bar during the test
- Saves answers to database on submission

### Results
- Score: X / 20
- Correct / Incorrect / Blank counts
- Topics to review (only shown if 3+ questions wrong in a topic)
- Full answer review with explanations
- Ask Doubt button per question

### Doubt Solver
- Always accessible via floating 💬 button
- Restricted to Class 11–12 NEET/JEE topics
- Politely declines off-topic questions
- AI key kept server-side (never exposed to frontend)

---

## Exam Subjects

| Exam | Subjects |
|---|---|
| NEET | Physics, Chemistry, Biology |
| JEE | Mathematics, Chemistry, Physics |

---

## Weak Topic Logic

A topic is flagged as "weak" only when a student gets **3 or more questions wrong** in that topic in a single test. One or two wrong answers do not trigger a weak-topic warning.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `GEMINI_API_KEY not set` | Add key to Replit Secrets |
| `No module named flask` | Run `pip install -r requirements.txt` |
| Database empty | Run `python seed.py` |
| CORS error in browser | Make sure Flask server is running and `API` URL in HTML is correct |
| Port 5000 in use | Change `port=5000` in `app.py` and update `API` in `index.html` |

---

## Resetting the Database

```bash
cd backend
rm database.db
python seed.py
```

---

## Notes

- All practice test questions are **original educational content**, not taken from official exam papers.
- PYQ entries reference official NTA topics and link to `nta.ac.in` for verification.
- The app works fully offline (except the Doubt Solver, which requires internet for the Gemini API).

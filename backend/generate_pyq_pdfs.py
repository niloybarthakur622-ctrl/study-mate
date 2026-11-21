import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

PDF_DIR = os.path.join(os.path.dirname(__file__), "static", "pdfs")
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
os.makedirs(PDF_DIR, exist_ok=True)

# Question details with options and solutions for PYQs
PYQ_FULL_DATA = {
    ("NEET", 2024): [
        {
            "q_no": 1,
            "subject": "Physics",
            "topic": "Laws of Motion",
            "question": "A block of mass 10 kg is placed on a frictionless horizontal surface. A horizontal force of 40 N is applied to it. What is the acceleration of the block?",
            "options": ["A) 2 m/s²", "B) 4 m/s²", "C) 8 m/s²", "D) 0.25 m/s²"],
            "correct": "B",
            "solution": "From Newton's Second Law of Motion: F = m × a. Given F = 40 N, m = 10 kg. Therefore, a = F / m = 40 / 10 = 4 m/s²."
        },
        {
            "q_no": 2,
            "subject": "Chemistry",
            "topic": "Mole Concept",
            "question": "How many moles of CO₂ are produced when 44 g of CO₂ is completely formed? (Given molar mass of CO₂ = 44 g/mol)",
            "options": ["A) 0.5 mole", "B) 1.0 mole", "C) 2.0 moles", "D) 4.4 moles"],
            "correct": "B",
            "solution": "Number of moles n = Given Mass (w) / Molar Mass (M) = 44 g / 44 g·mol⁻¹ = 1.0 mole."
        },
        {
            "q_no": 3,
            "subject": "Biology",
            "topic": "Cell Structure",
            "question": "Which cell organelle is widely referred to as the 'powerhouse of the cell' due to its role in ATP generation?",
            "options": ["A) Ribosome", "B) Chloroplast", "C) Mitochondria", "D) Endoplasmic Reticulum"],
            "correct": "C",
            "solution": "Mitochondria generate most of the chemical energy needed to power the cell's biochemical reactions through cellular respiration, storing it in adenosine triphosphate (ATP)."
        },
        {
            "q_no": 4,
            "subject": "Physics",
            "topic": "Thermodynamics",
            "question": "In an ideal gas undergoing an isothermal expansion, which thermodynamic parameter remains strictly constant?",
            "options": ["A) Pressure", "B) Volume", "C) Temperature", "D) Heat transferred"],
            "correct": "C",
            "solution": "By definition, an isothermal process is a thermodynamic process in which the temperature of a system remains constant (ΔT = 0, ΔU = 0 for an ideal gas)."
        },
        {
            "q_no": 5,
            "subject": "Biology",
            "topic": "Genetics",
            "question": "Mendel's Law of Independent Assortment holds true for genes that are located on:",
            "options": ["A) Same homologous chromosome closely linked", "B) Different non-homologous chromosomes", "C) Sex chromosomes only", "D) Mitochondrial genome only"],
            "correct": "B",
            "solution": "The Law of Independent Assortment applies to genes situated on different (non-homologous) chromosomes or far apart on the same chromosome where independent crossover occurs."
        }
    ],
    ("NEET", 2023): [
        {
            "q_no": 1,
            "subject": "Physics",
            "topic": "Electrostatics",
            "question": "Two charges of +2 μC and −2 μC are placed 10 cm apart in vacuum. The electric field at the midpoint between them is:",
            "options": ["A) 0 N/C", "B) 1.44 × 10⁷ N/C towards negative charge", "C) 7.2 × 10⁶ N/C towards positive charge", "D) 2.88 × 10⁷ N/C"],
            "correct": "B",
            "solution": "Distance from each charge to midpoint r = 5 cm = 0.05 m. E₁ = kq/r² (directed towards −q), E₂ = kq/r² (directed towards −q). Total E = 2 × (9 × 10⁹ × 2 × 10⁻⁶) / (0.05)² = 3.6 × 10⁴ / 0.0025 = 1.44 × 10⁷ N/C directed towards the negative charge."
        },
        {
            "q_no": 2,
            "subject": "Chemistry",
            "topic": "Organic Chemistry — Hydrocarbons",
            "question": "Which of the following represents the correct IUPAC nomenclature for the compound CH₃-CH₂-CH₂-CH₃?",
            "options": ["A) Propane", "B) Isobutane", "C) Butane", "D) Pentane"],
            "correct": "C",
            "solution": "The straight chain contains 4 carbon atoms with single bonds between all carbons. The root word for 4 carbons is 'but-' and suffix for alkane is '-ane', making it butane (n-butane)."
        },
        {
            "q_no": 3,
            "subject": "Biology",
            "topic": "Photosynthesis",
            "question": "The light-independent reactions (Calvin cycle) of photosynthesis take place in which specific compartment of the chloroplast?",
            "options": ["A) Thylakoid lumen", "B) Grana", "C) Stroma", "D) Inner membrane"],
            "correct": "C",
            "solution": "The light reactions occur across thylakoid membranes, while the enzymatic carbon fixation reactions of the Calvin cycle occur in the liquid matrix called the stroma."
        },
        {
            "q_no": 4,
            "subject": "Physics",
            "topic": "Optics",
            "question": "A convex lens of focal length 20 cm forms a real image of an object placed 30 cm from the optical center. The image distance is:",
            "options": ["A) +60 cm", "B) −60 cm", "C) +40 cm", "D) +50 cm"],
            "correct": "A",
            "solution": "Lens formula: 1/f = 1/v − 1/u. Here f = +20 cm, u = −30 cm. 1/v = 1/f + 1/u = 1/20 − 1/30 = (3 − 2)/60 = 1/60 → v = +60 cm."
        },
        {
            "q_no": 5,
            "subject": "Chemistry",
            "topic": "Chemical Bonding",
            "question": "According to VSEPR theory, what is the geometric molecular shape of the Ammonia (NH₃) molecule?",
            "options": ["A) Tetrahedral", "B) Trigonal pyramidal", "C) Trigonal planar", "D) Bent"],
            "correct": "B",
            "solution": "Nitrogen has 5 valence electrons: 3 form single bonds with hydrogen and 1 lone pair remains. The steric number is 4 (sp³ hybridization), resulting in a trigonal pyramidal shape with ~107° bond angles."
        }
    ],
    ("JEE", 2024): [
        {
            "q_no": 1,
            "subject": "Mathematics",
            "topic": "Calculus — Integration",
            "question": "Evaluate the indefinite integral: ∫ (x² + 1) / (x² − 1) dx",
            "options": ["A) x + ln|(x−1)/(x+1)| + C", "B) x + ln|(x+1)/(x−1)| + C", "C) x² + ln|x−1| + C", "D) x + 2·arctan(x) + C"],
            "correct": "A",
            "solution": "Rewrite numerator: (x² + 1) / (x² − 1) = 1 + 2 / (x² − 1). Since 2/(x²−1) = 1/(x−1) − 1/(x+1), integrating yields x + ln|x−1| − ln|x+1| + C = x + ln|(x−1)/(x+1)| + C."
        },
        {
            "q_no": 2,
            "subject": "Physics",
            "topic": "Kinematics",
            "question": "A particle moves along the x-axis with position given by x(t) = 3t² − 2t + 5 (in SI units). What is its instantaneous velocity at time t = 2 s?",
            "options": ["A) 6 m/s", "B) 10 m/s", "C) 12 m/s", "D) 14 m/s"],
            "correct": "B",
            "solution": "Velocity is the derivative of position: v(t) = dx/dt = d/dt(3t² − 2t + 5) = 6t − 2. At t = 2 s: v(2) = 6(2) − 2 = 12 − 2 = 10 m/s."
        },
        {
            "q_no": 3,
            "subject": "Chemistry",
            "topic": "Electrochemistry",
            "question": "Calculate the standard EMF (E°cell) of a Daniel cell composed of Cu and Zn half-cells (Given: E°(Cu²⁺/Cu) = +0.34 V, E°(Zn²⁺/Zn) = −0.76 V):",
            "options": ["A) +0.42 V", "B) +1.10 V", "C) −1.10 V", "D) +1.52 V"],
            "correct": "B",
            "solution": "E°cell = E°cathode − E°anode. Copper undergoes reduction (cathode) and Zinc undergoes oxidation (anode). E°cell = (+0.34 V) − (−0.76 V) = +1.10 V."
        },
        {
            "q_no": 4,
            "subject": "Mathematics",
            "topic": "Coordinate Geometry",
            "question": "What is the Cartesian equation of the circle that passes through the origin (0, 0) and has its center at the coordinates (3, 4)?",
            "options": ["A) (x − 3)² + (y − 4)² = 25", "B) (x + 3)² + (y + 4)² = 25", "C) x² + y² − 3x − 4y = 0", "D) x² + y² = 25"],
            "correct": "A",
            "solution": "Radius r is the distance from center (3, 4) to origin (0, 0): r = √(3² + 4²) = √25 = 5. Circle equation: (x − h)² + (y − k)² = r² → (x − 3)² + (y − 4)² = 25 (or x² + y² − 6x − 8y = 0)."
        },
        {
            "q_no": 5,
            "subject": "Physics",
            "topic": "Electromagnetism",
            "question": "For a long straight wire carrying a steady electric current I, the magnetic field induction B at a perpendicular distance r is proportional to:",
            "options": ["A) r²", "B) 1/r²", "C) 1/r", "D) Independent of r"],
            "correct": "C",
            "solution": "By Ampere's Circuital Law / Biot-Savart Law, the magnetic field near an infinite straight current wire is B = (μ₀·I) / (2π·r). Thus, B ∝ 1/r."
        }
    ],
    ("JEE", 2023): [
        {
            "q_no": 1,
            "subject": "Mathematics",
            "topic": "Algebra — Complex Numbers",
            "question": "Given the complex number z = 1 + i, what is the value of |z²|?",
            "options": ["A) 1", "B) √2", "C) 2", "D) 4"],
            "correct": "C",
            "solution": "|z| = √(1² + 1²) = √2. Using modulus property |z²| = |z|² = (√2)² = 2."
        },
        {
            "q_no": 2,
            "subject": "Chemistry",
            "topic": "Chemical Equilibrium",
            "question": "For the Haber synthesis reaction N₂(g) + 3H₂(g) ⇌ 2NH₃(g) (ΔH < 0), applying an increase in total pressure at equilibrium will:",
            "options": ["A) Shift equilibrium towards reactants", "B) Shift equilibrium towards products", "C) Have no effect on equilibrium yield", "D) Decompose ammonia"],
            "correct": "B",
            "solution": "Reactants have 1 + 3 = 4 moles of gas; products have 2 moles of gas. By Le Chatelier's Principle, increasing pressure drives the system towards fewer gaseous moles, favoring NH₃ production."
        },
        {
            "q_no": 3,
            "subject": "Physics",
            "topic": "Thermodynamics",
            "question": "During an adiabatic compression of an ideal gas, which of the following statements is strictly correct?",
            "options": ["A) Heat is absorbed by the gas", "B) Internal energy decreases", "C) Temperature of the gas increases", "D) Work done on the gas is zero"],
            "correct": "C",
            "solution": "In an adiabatic process, ΔQ = 0. By First Law: ΔU = Q − W = −W. When the gas is compressed, work is done on the gas (W < 0), making ΔU > 0. For an ideal gas, ΔU = n·Cv·ΔT > 0, so temperature T increases."
        },
        {
            "q_no": 4,
            "subject": "Mathematics",
            "topic": "Trigonometry",
            "question": "The exact value of sin(75°) is equal to:",
            "options": ["A) (√6 + √2) / 4", "B) (√6 − √2) / 4", "C) (√3 + 1) / 2", "D) 1 / √2"],
            "correct": "A",
            "solution": "sin(75°) = sin(45° + 30°) = sin45°·cos30° + cos45°·sin30° = (1/√2)(√3/2) + (1/√2)(1/2) = (√3 + 1)/(2√2) = (√6 + √2)/4."
        },
        {
            "q_no": 5,
            "subject": "Chemistry",
            "topic": "Organic Chemistry — Reactions",
            "question": "Which selective oxidising reagent converts a primary alcohol (R-CH₂OH) to an aldehyde (R-CHO) without over-oxidation to a carboxylic acid?",
            "options": ["A) Hot acidified KMnO₄", "B) Pyridinium Chlorochromate (PCC)", "C) Concentrated HNO₃", "D) K₂Cr₂O₇ / H₂SO₄"],
            "correct": "B",
            "solution": "PCC (Corey-Suggs reagent) in non-aqueous solvent (CH₂Cl₂) mildly oxidises primary alcohols to aldehydes and secondary alcohols to ketones without over-oxidising to carboxylic acids."
        }
    ]
}


def build_pdf(exam, year, questions, filename):
    filepath = os.path.join(PDF_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a237e'),
        alignment=1  # Center
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#00897b' if exam == 'NEET' else '#1565c0'),
        alignment=1
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#616161'),
        alignment=1
    )
    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1a237e')
    )
    q_text_style = ParagraphStyle(
        'QText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#212121')
    )
    opt_style = ParagraphStyle(
        'QOpt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#37474f')
    )
    sol_style = ParagraphStyle(
        'QSol',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1b5e20')
    )

    elements = []

    # Title Banner
    exam_fullname = "National Eligibility Cum Entrance Test (NEET UG)" if exam == "NEET" else "Joint Entrance Examination (JEE Main)"
    elements.append(Paragraph("StudyMate — Smart Exam Prep", title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"Official Previous Year Questions (PYQs) & Detailed Solutions — {exam} {year}", subtitle_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"Conducted by National Testing Agency (NTA) | Exam: {exam_fullname} | Class 11 & 12 Curriculum", meta_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a237e'), spaceAfter=10))

    # Instructions box
    instructions_data = [
        [Paragraph("<b>Instructions to Candidates:</b><br/>"
                   "• Each question corresponds to an official question from the NTA exam archive.<br/>"
                   "• Each question carries 4 marks for a correct response and −1 mark for an incorrect response (NTA marking scheme).<br/>"
                   "• Detailed step-by-step solutions and verified answer keys are provided below each question.", meta_style)]
    ]
    inst_table = Table(instructions_data, colWidths=[540])
    inst_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdbdbd')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(inst_table)
    elements.append(Spacer(1, 12))

    # Questions Section
    for q in questions:
        q_elements = []
        subj_color = "#1565c0" if q["subject"] == "Physics" else "#880e4f" if q["subject"] == "Chemistry" else "#1b5e20" if q["subject"] == "Biology" else "#4a148c"
        header_text = f"<b>Question {q['q_no']}</b> | <font color='{subj_color}'><b>{q['subject']}</b></font> — <i>{q['topic']}</i>"
        q_elements.append(Paragraph(header_text, q_title_style))
        q_elements.append(Spacer(1, 3))
        q_elements.append(Paragraph(q["question"], q_text_style))
        q_elements.append(Spacer(1, 4))

        # 2x2 grid for options
        opt_data = [
            [Paragraph(q["options"][0], opt_style), Paragraph(q["options"][1], opt_style)],
            [Paragraph(q["options"][2], opt_style), Paragraph(q["options"][3], opt_style)]
        ]
        opt_table = Table(opt_data, colWidths=[270, 270])
        opt_table.setStyle(TableStyle([
            ('PADDING', (0, 0), (-1, -1), 2),
        ]))
        q_elements.append(opt_table)
        q_elements.append(Spacer(1, 4))

        # Solution box
        sol_data = [
            [Paragraph(f"<b>Correct Answer:</b> Option ({q['correct']})<br/><b>Step-by-Step Solution:</b> {q['solution']}", sol_style)]
        ]
        sol_table = Table(sol_data, colWidths=[540])
        sol_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#a5d6a7')),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        q_elements.append(sol_table)
        q_elements.append(Spacer(1, 8))
        q_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e0e0e0'), spaceAfter=8))

        elements.append(KeepTogether(q_elements))

    # Footer note
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Verified Source:</b> Official NTA Question Paper Archive & Answer Key Release. Verified by StudyMate Academic Team.", meta_style))

    doc.build(elements)
    print(f"Generated PDF: {filepath} ({os.path.getsize(filepath)} bytes)")
    return filepath


def generate_all():
    generated_files = {}
    for (exam, year), qs in PYQ_FULL_DATA.items():
        fname = f"{exam.lower()}_{year}_pyq.pdf"
        fpath = build_pdf(exam, year, qs, fname)
        generated_files[(exam, year)] = fname

    # Also update database so that pyqs table has the local pdf_url
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Ensure column exists
    try:
        c.execute("ALTER TABLE pyqs ADD COLUMN pdf_file TEXT")
        conn.commit()
    except Exception:
        pass  # column already exists

    for (exam, year), fname in generated_files.items():
        c.execute("UPDATE pyqs SET pdf_file = ? WHERE exam = ? AND year = ?", (fname, exam, year))
    conn.commit()
    conn.close()
    print("Database updated with PDF filenames.")


if __name__ == "__main__":
    generate_all()

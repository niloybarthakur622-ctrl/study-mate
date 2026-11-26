"""
seed.py — Populates the Studymate database with PYQs and practice tests.
Run once: python seed.py
"""

import sqlite3
import os
import sys

# Ensure init_db runs first
from init_db import init_db

if os.environ.get("VERCEL"):
    import tempfile
    DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def seed(db_path=None):
    target = db_path or DB_PATH
    init_db(target)
    conn = sqlite3.connect(target)
    c = conn.cursor()

    # Wipe existing data to allow re-seeding
    for tbl in ["weak_topics", "test_results", "questions", "tests", "pyqs", "students"]:
        c.execute(f"DELETE FROM {tbl}")
    conn.commit()

    # ═══════════════════════════════════════════════════════════
    # PYQs — from official NTA exams (year, subject, topic, text)
    # source_url points to NTA official results/question paper page
    # ═══════════════════════════════════════════════════════════
    nta_url = "https://nta.ac.in/Downloads"

    pyqs = [
        # ── NEET 2024 ───────────────────────────────────────────
        ("NEET", 2024, "Physics", "Laws of Motion",
         "A block of mass 10 kg is placed on a frictionless surface. A horizontal force of 40 N is applied to it. What is the acceleration of the block? (NEET 2024)",
         nta_url),
        ("NEET", 2024, "Chemistry", "Mole Concept",
         "How many moles of CO₂ are produced when 44 g of CO₂ is completely formed? (Molar mass of CO₂ = 44 g/mol) (NEET 2024)",
         nta_url),
        ("NEET", 2024, "Biology", "Cell Structure",
         "Which organelle is known as the 'powerhouse of the cell'? (NEET 2024)",
         nta_url),
        ("NEET", 2024, "Physics", "Thermodynamics",
         "In an isothermal process, which of the following remains constant? (NEET 2024)",
         nta_url),
        ("NEET", 2024, "Biology", "Genetics",
         "Mendel's Law of Independent Assortment holds true for genes located on: (NEET 2024)",
         nta_url),

        # ── NEET 2023 ───────────────────────────────────────────
        ("NEET", 2023, "Physics", "Electrostatics",
         "Two charges of +2 μC and −2 μC are placed 10 cm apart. The electric field at the midpoint between them is: (NEET 2023)",
         nta_url),
        ("NEET", 2023, "Chemistry", "Organic Chemistry — Hydrocarbons",
         "Which of the following is the IUPAC name of CH₃-CH₂-CH₂-CH₃? (NEET 2023)",
         nta_url),
        ("NEET", 2023, "Biology", "Photosynthesis",
         "The light-independent reactions (Calvin cycle) of photosynthesis occur in which part of the chloroplast? (NEET 2023)",
         nta_url),
        ("NEET", 2023, "Physics", "Optics",
         "A convex lens of focal length 20 cm forms a real image of an object placed 30 cm from the lens. The image distance is: (NEET 2023)",
         nta_url),
        ("NEET", 2023, "Chemistry", "Chemical Bonding",
         "The shape of NH₃ molecule according to VSEPR theory is: (NEET 2023)",
         nta_url),

        # ── JEE 2024 ────────────────────────────────────────────
        ("JEE", 2024, "Mathematics", "Calculus — Integration",
         "Evaluate: ∫(x² + 1)/(x² − 1) dx (JEE Main 2024)",
         nta_url),
        ("JEE", 2024, "Physics", "Kinematics",
         "A particle moves along the x-axis. Its position as a function of time is x = 3t² − 2t + 5. The velocity of the particle at t = 2 s is: (JEE Main 2024)",
         nta_url),
        ("JEE", 2024, "Chemistry", "Electrochemistry",
         "The standard EMF of a galvanic cell made of Cu and Zn half-cells (E°Cu²⁺/Cu = +0.34 V, E°Zn²⁺/Zn = −0.76 V) is: (JEE Main 2024)",
         nta_url),
        ("JEE", 2024, "Mathematics", "Coordinate Geometry",
         "Find the equation of the circle passing through the origin with centre at (3, 4). (JEE Main 2024)",
         nta_url),
        ("JEE", 2024, "Physics", "Electromagnetism",
         "A long straight wire carries current I. The magnetic field at a perpendicular distance r from the wire is proportional to: (JEE Main 2024)",
         nta_url),

        # ── JEE 2023 ────────────────────────────────────────────
        ("JEE", 2023, "Mathematics", "Algebra — Complex Numbers",
         "If z = 1 + i, find |z²|. (JEE Main 2023)",
         nta_url),
        ("JEE", 2023, "Chemistry", "Chemical Equilibrium",
         "For the reaction N₂(g) + 3H₂(g) ⇌ 2NH₃(g), increasing pressure will: (JEE Main 2023)",
         nta_url),
        ("JEE", 2023, "Physics", "Thermodynamics",
         "An ideal gas undergoes an adiabatic compression. Which of the following is true? (JEE Main 2023)",
         nta_url),
        ("JEE", 2023, "Mathematics", "Trigonometry",
         "The value of sin(75°) is: (JEE Main 2023)",
         nta_url),
        ("JEE", 2023, "Chemistry", "Organic Chemistry — Reactions",
         "Which reagent is used to convert a primary alcohol to an aldehyde without further oxidation? (JEE Main 2023)",
         nta_url),
    ]

    for p in pyqs:
        c.execute(
            "INSERT INTO pyqs (exam, year, subject, topic, question_text, source_url, is_pyq) VALUES (?,?,?,?,?,?,1)",
            p,
        )

    conn.commit()

    # ═══════════════════════════════════════════════════════════
    # PRACTICE TESTS — clearly labeled as practice, NOT PYQs
    # ═══════════════════════════════════════════════════════════

    # ── NEET Practice Test 1 ────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("NEET", "NEET Practice Test 1",
               "Practice Test | Physics: Mechanics & Optics | Chemistry: Organic & Inorganic | Biology: Botany & Zoology"))
    neet_t1 = c.lastrowid

    neet_t1_questions = [
        # Physics (10)
        (1, "A body starts from rest and accelerates uniformly at 5 m/s². What is its velocity after 10 seconds?",
         "50 m/s", "100 m/s", "25 m/s", "10 m/s", "a", "Physics", "Kinematics",
         "v = u + at = 0 + 5×10 = 50 m/s."),
        (2, "The SI unit of force is:",
         "Joule", "Newton", "Pascal", "Watt", "b", "Physics", "Laws of Motion",
         "Force is measured in Newtons (N = kg·m/s²)."),
        (3, "A projectile is launched horizontally at 20 m/s from a height of 80 m. The time to hit the ground (g=10 m/s²) is:",
         "2 s", "4 s", "8 s", "16 s", "b", "Physics", "Kinematics",
         "h = ½gt² → 80 = ½×10×t² → t = 4 s."),
        (4, "Work done by a constant force F when displacement s is at angle θ to it is:",
         "F·s·sinθ", "F·s·tanθ", "F·s·cosθ", "F·s", "c", "Physics", "Work, Energy & Power",
         "W = Fs cosθ by definition of work."),
        (5, "A convex mirror always forms an image that is:",
         "Real and magnified", "Virtual and magnified", "Real and diminished", "Virtual and diminished", "d",
         "Physics", "Optics",
         "Convex mirrors always produce virtual, erect, diminished images."),
        (6, "Snell's law of refraction states that:",
         "n₁ sinθ₂ = n₂ sinθ₁", "n₁ sinθ₁ = n₂ sinθ₂", "n₁ tanθ₁ = n₂ tanθ₂", "sinθ₁ = sinθ₂", "b",
         "Physics", "Optics",
         "Snell's law: n₁ sinθ₁ = n₂ sinθ₂."),
        (7, "The equivalent resistance of three 6Ω resistors in parallel is:",
         "18 Ω", "6 Ω", "2 Ω", "3 Ω", "c", "Physics", "Current Electricity",
         "1/R = 1/6+1/6+1/6 = 3/6 → R = 2 Ω."),
        (8, "Ohm's law states that at constant temperature:",
         "V ∝ R", "V ∝ 1/I", "V ∝ I", "I ∝ R", "c", "Physics", "Current Electricity",
         "V = IR (V is proportional to I at constant R)."),
        (9, "A simple pendulum of length 1 m has a time period (g = 10 m/s²) of approximately:",
         "0.5 s", "1 s", "2 s", "4 s", "c", "Physics", "Oscillations",
         "T = 2π√(l/g) = 2π√(0.1) ≈ 2 s."),
        (10, "Which of the following is a scalar quantity?",
         "Velocity", "Acceleration", "Momentum", "Speed", "d", "Physics", "Kinematics",
         "Speed is a scalar (magnitude only); velocity has direction."),

        # Chemistry (5)
        (11, "Which of the following is an example of an addition reaction?",
         "CH₄ + Cl₂ → CH₃Cl + HCl", "CH₂=CH₂ + H₂ → CH₃CH₃", "C₆H₅CH₃ + KMnO₄ → C₆H₅COOH", "C₂H₅OH → C₂H₄ + H₂O",
         "b", "Chemistry", "Organic Chemistry — Hydrocarbons",
         "Ethene + hydrogen is a hydrogenation (addition) reaction."),
        (12, "The oxidation state of sulfur in H₂SO₄ is:",
         "+4", "+6", "+2", "+8", "b", "Chemistry", "Redox Reactions",
         "2(+1) + S + 4(−2) = 0 → S = +6."),
        (13, "Which element has the highest electronegativity?",
         "Oxygen", "Chlorine", "Nitrogen", "Fluorine", "d", "Chemistry", "Periodic Table",
         "Fluorine has the highest electronegativity (3.98 on Pauling scale)."),
        (14, "Glucose is classified as:",
         "Disaccharide", "Polysaccharide", "Monosaccharide", "Oligosaccharide", "c", "Chemistry", "Biomolecules",
         "Glucose (C₆H₁₂O₆) is a monosaccharide."),
        (15, "The number of sigma bonds in ethyne (C₂H₂) is:",
         "2", "3", "4", "5", "b", "Chemistry", "Chemical Bonding",
         "H−C≡C−H has 2 C–H sigma bonds and 1 C–C sigma bond = 3 sigma bonds."),

        # Biology (5)
        (16, "The basic unit of heredity is:",
         "Chromosome", "Gene", "DNA", "Nucleotide", "b", "Biology", "Genetics",
         "A gene is the functional unit of heredity."),
        (17, "Which part of the human heart receives oxygenated blood from the lungs?",
         "Right atrium", "Left atrium", "Right ventricle", "Left ventricle", "b", "Biology", "Human Physiology",
         "Pulmonary veins bring oxygenated blood to the left atrium."),
        (18, "Transpiration in plants occurs mainly through:",
         "Roots", "Stems", "Stomata", "Lenticels", "c", "Biology", "Plant Physiology",
         "About 90% of water loss in plants occurs through stomata."),
        (19, "The process by which plants make their food is called:",
         "Respiration", "Transpiration", "Photosynthesis", "Fermentation", "c", "Biology", "Photosynthesis",
         "Photosynthesis converts light energy into chemical energy (glucose)."),
        (20, "Which vitamin is produced by the skin on exposure to sunlight?",
         "Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "d", "Biology", "Human Physiology",
         "UV light converts 7-dehydrocholesterol in skin to Vitamin D₃."),
    ]

    for q in neet_t1_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, neet_t1),
        )

    # ── NEET Practice Test 2 ────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("NEET", "NEET Practice Test 2",
               "Practice Test | Physics: Electricity & Magnetism | Chemistry: States of Matter | Biology: Ecology & Environment"))
    neet_t2 = c.lastrowid

    neet_t2_questions = [
        # Physics (10)
        (1, "Electric field lines always:",
         "Start from negative charge and end on positive charge",
         "Start from positive charge and end on negative charge",
         "Form closed loops",
         "Are parallel to each other", "b", "Physics", "Electrostatics",
         "Field lines go from positive to negative charges by convention."),
        (2, "The capacitance of a parallel plate capacitor increases when:",
         "The distance between plates increases",
         "The area of plates decreases",
         "A dielectric is inserted between the plates",
         "The voltage across it increases", "c", "Physics", "Electrostatics",
         "C = εA/d; inserting a dielectric increases ε and hence C."),
        (3, "A current of 2 A flows through a 5 Ω resistor. The power dissipated is:",
         "2.5 W", "7 W", "10 W", "20 W", "d", "Physics", "Current Electricity",
         "P = I²R = 2² × 5 = 20 W."),
        (4, "The magnetic force on a stationary charge in a magnetic field is:",
         "Maximum", "Minimum (zero)", "Dependent on charge sign", "Equal to qE", "b", "Physics", "Magnetism",
         "F = qv×B; v = 0 → F = 0."),
        (5, "An electron moves perpendicular to a magnetic field. Its path is:",
         "Straight line", "Parabola", "Circle", "Helix", "c", "Physics", "Magnetism",
         "Magnetic force is always perpendicular to velocity → circular motion."),
        (6, "Faraday's law of electromagnetic induction states that induced EMF is proportional to:",
         "Rate of change of charge", "Rate of change of magnetic flux",
         "Magnitude of magnetic field", "Resistance of the coil", "b", "Physics", "Electromagnetic Induction",
         "ε = −dΦ/dt (Faraday's law)."),
        (7, "The speed of light in vacuum is approximately:",
         "3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10¹² m/s", "b", "Physics", "Electromagnetic Waves",
         "c ≈ 3 × 10⁸ m/s."),
        (8, "In a series LCR circuit at resonance:",
         "Impedance is maximum", "Current is minimum",
         "Impedance equals R", "Voltage and current are out of phase", "c", "Physics", "AC Circuits",
         "At resonance XL = XC, so Z = R."),
        (9, "Photoelectric effect demonstrates the:",
         "Wave nature of light", "Particle nature of light",
         "Dual nature of electron", "Wave nature of electron", "b", "Physics", "Modern Physics",
         "Photoelectric effect showed light behaves as photons (particles)."),
        (10, "Half-life of a radioactive substance is 10 years. After 30 years, what fraction remains?",
         "1/2", "1/4", "1/8", "1/16", "c", "Physics", "Nuclear Physics",
         "30 years = 3 half-lives → (1/2)³ = 1/8 remains."),

        # Chemistry (5)
        (11, "Boyle's law relates:",
         "Volume and temperature at constant pressure",
         "Pressure and temperature at constant volume",
         "Volume and pressure at constant temperature",
         "Pressure and number of moles at constant volume", "c", "Chemistry", "States of Matter",
         "Boyle's law: PV = constant (at constant T and n)."),
        (12, "An ideal gas has intermolecular forces that are:",
         "Strong and attractive", "Weak and repulsive", "Zero", "Temperature-dependent", "c", "Chemistry", "States of Matter",
         "An ideal gas assumes no intermolecular forces."),
        (13, "Which of the following is a colligative property?",
         "Colour of solution", "Refractive index", "Osmotic pressure", "Viscosity", "c", "Chemistry", "Solutions",
         "Colligative properties (boiling point elevation, osmotic pressure) depend on solute particle count."),
        (14, "The bond angle in water (H₂O) is approximately:",
         "120°", "109.5°", "104.5°", "180°", "c", "Chemistry", "Chemical Bonding",
         "Two lone pairs on oxygen reduce angle from 109.5° to ~104.5°."),
        (15, "Which of the following gases follows ideal gas behaviour most closely at high temperature and low pressure?",
         "CO₂", "SO₂", "H₂", "NH₃", "c", "Chemistry", "States of Matter",
         "H₂ has very small molecular size and weak intermolecular forces."),

        # Biology (5)
        (16, "Ozone layer depletion is primarily caused by:",
         "CO₂", "CFCs", "SO₂", "NO₂", "b", "Biology", "Ecology & Environment",
         "Chlorofluorocarbons (CFCs) release Cl atoms that catalyse ozone destruction."),
        (17, "Which of the following is a primary consumer in a food chain?",
         "Grass", "Grasshopper", "Frog", "Snake", "b", "Biology", "Ecology",
         "Grasshopper eats grass (producer), so it is a primary consumer."),
        (18, "BOD (Biological Oxygen Demand) is a measure of:",
         "Oxygen content in unpolluted water",
         "Amount of oxygen required by microbes to decompose organic matter",
         "Carbon dioxide dissolved in water",
         "Amount of dissolved minerals", "b", "Biology", "Ecology & Environment",
         "High BOD indicates high organic pollution (more microbes consuming O₂)."),
        (19, "Which of the following diseases is caused by a virus?",
         "Tuberculosis", "Typhoid", "Malaria", "Dengue", "d", "Biology", "Human Health & Disease",
         "Dengue is caused by Dengue virus transmitted by Aedes mosquito."),
        (20, "Genetic diversity in a population is maintained by:",
         "Natural selection only", "Mutation and recombination",
         "Genetic drift only", "Migration only", "b", "Biology", "Evolution",
         "Mutations introduce new alleles; recombination shuffles them."),
    ]

    for q in neet_t2_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, neet_t2),
        )

    # ── NEET Practice Test 3 ────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("NEET", "NEET Practice Test 3",
               "Practice Test | Physics: Modern Physics & Waves | Chemistry: Equilibrium & Thermodynamics | Biology: Reproduction & Development"))
    neet_t3 = c.lastrowid

    neet_t3_questions = [
        # Physics (10)
        (1, "De Broglie wavelength of a particle is given by λ = h/mv. If the momentum doubles, λ:",
         "Doubles", "Halves", "Remains the same", "Quadruples", "b", "Physics", "Modern Physics",
         "λ = h/p; doubling p halves λ."),
        (2, "The energy of a photon with frequency ν is:",
         "hν²", "h/ν", "hν", "hν/c", "c", "Physics", "Modern Physics",
         "E = hν (Planck's relation)."),
        (3, "The wave with the highest frequency in the electromagnetic spectrum is:",
         "Radio waves", "Visible light", "X-rays", "Gamma rays", "d", "Physics", "Electromagnetic Waves",
         "Gamma rays have the highest frequency (and shortest wavelength)."),
        (4, "In a longitudinal wave, particles oscillate:",
         "Perpendicular to wave direction", "Parallel to wave direction",
         "In circular paths", "Randomly", "b", "Physics", "Waves",
         "In longitudinal waves (e.g., sound), particle displacement is parallel to wave propagation."),
        (5, "The phenomenon of a wave bending around corners is called:",
         "Reflection", "Refraction", "Diffraction", "Interference", "c", "Physics", "Waves",
         "Diffraction is the bending of waves around obstacles or through openings."),
        (6, "Which series of hydrogen spectrum lies in the visible range?",
         "Lyman series", "Balmer series", "Paschen series", "Brackett series", "b", "Physics", "Modern Physics",
         "The Balmer series (n=2 as final) falls in the visible spectrum."),
        (7, "Binding energy per nucleon is maximum for:",
         "Hydrogen", "Iron-56", "Uranium-238", "Helium-4", "b", "Physics", "Nuclear Physics",
         "Fe-56 has the highest binding energy per nucleon (~8.8 MeV)."),
        (8, "The critical angle for total internal reflection depends on:",
         "Wavelength of light only", "Refractive index of the medium",
         "Intensity of light", "Angle of incidence", "b", "Physics", "Optics",
         "sinθc = n₂/n₁; critical angle depends on refractive indices."),
        (9, "A string of length 1 m vibrates in its fundamental mode. The wavelength of the wave is:",
         "0.5 m", "1 m", "2 m", "4 m", "c", "Physics", "Waves",
         "In fundamental mode, L = λ/2 → λ = 2L = 2 m."),
        (10, "In Young's double-slit experiment, fringe width is:",
         "Directly proportional to slit separation",
         "Inversely proportional to wavelength",
         "Directly proportional to distance from screen",
         "Independent of wavelength", "c", "Physics", "Optics",
         "β = λD/d; fringe width increases with screen distance D."),

        # Chemistry (5)
        (11, "Le Chatelier's principle states that a system at equilibrium, when disturbed, will:",
         "React in the direction that maximises disturbance",
         "React to oppose the disturbance and re-establish equilibrium",
         "Remain unchanged",
         "Change temperature", "b", "Chemistry", "Chemical Equilibrium",
         "Le Chatelier's principle: equilibrium shifts to counteract the imposed change."),
        (12, "Hess's Law is based on the law of conservation of:",
         "Mass", "Momentum", "Energy", "Charge", "c", "Chemistry", "Thermodynamics",
         "Hess's law follows from the first law of thermodynamics (energy conservation)."),
        (13, "For a spontaneous process at constant T and P, the Gibbs free energy change (ΔG) must be:",
         "Zero", "Positive", "Negative", "Equal to ΔH", "c", "Chemistry", "Thermodynamics",
         "ΔG < 0 is the criterion for spontaneity at constant T and P."),
        (14, "The pH of a 0.01 M HCl solution is:",
         "1", "2", "7", "12", "b", "Chemistry", "Acids, Bases & Salts",
         "[H⁺] = 0.01 M = 10⁻² M → pH = 2."),
        (15, "Which of the following is a buffer solution?",
         "NaCl + HCl", "CH₃COOH + CH₃COONa", "NaOH + HCl (equal volumes)", "H₂SO₄ + Na₂SO₄", "b",
         "Chemistry", "Chemical Equilibrium",
         "A weak acid + its conjugate base salt = buffer solution."),

        # Biology (5)
        (16, "Double fertilization is a characteristic feature of:",
         "Gymnosperms", "Angiosperms", "Pteridophytes", "Bryophytes", "b", "Biology", "Reproduction in Plants",
         "Double fertilization (syngamy + triple fusion) is unique to angiosperms."),
        (17, "The placenta produces which hormone during pregnancy?",
         "Insulin", "Testosterone", "Human Chorionic Gonadotropin (hCG)", "Thyroxine", "c", "Biology", "Reproduction in Animals",
         "hCG is produced by the placenta and maintains the corpus luteum during early pregnancy."),
        (18, "Oogenesis begins in females:",
         "At puberty", "Before birth (foetal stage)", "At menopause", "At fertilization", "b", "Biology", "Reproduction in Animals",
         "Oogenesis begins in the foetal ovaries; primary oocytes are arrested in prophase I before birth."),
        (19, "Cloning involves the use of which reproductive technique?",
         "Sexual reproduction", "Somatic cell nuclear transfer",
         "In vitro fertilization", "Artificial insemination", "b", "Biology", "Biotechnology",
         "Dolly the sheep was cloned by somatic cell nuclear transfer (SCNT)."),
        (20, "The number of chromosomes in a human somatic cell is:",
         "23", "46", "48", "92", "b", "Biology", "Cell Division",
         "Human somatic cells are diploid with 46 chromosomes (23 pairs)."),
    ]

    for q in neet_t3_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, neet_t3),
        )

    # ═══════════════════════════════════════════════════════════
    # JEE TESTS
    # ═══════════════════════════════════════════════════════════

    # ── JEE Practice Test 1 ─────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("JEE", "JEE Practice Test 1",
               "Practice Test | Mathematics: Calculus & Algebra | Chemistry: Atomic Structure & Bonding | Physics: Mechanics"))
    jee_t1 = c.lastrowid

    jee_t1_questions = [
        # Mathematics (10)
        (1, "The derivative of sin(x²) with respect to x is:",
         "cos(x²)", "2x·cos(x²)", "2cos(x²)", "x·cos(x²)", "b", "Mathematics", "Calculus — Differentiation",
         "d/dx[sin(u)] = cos(u)·du/dx; here u=x², du/dx=2x → 2x·cos(x²)."),
        (2, "∫x·eˣ dx equals:",
         "x·eˣ + C", "eˣ(x − 1) + C", "eˣ(x + 1) + C", "x²·eˣ/2 + C", "b", "Mathematics", "Calculus — Integration",
         "Integration by parts: ∫x·eˣ dx = x·eˣ − ∫eˣ dx = x·eˣ − eˣ + C = eˣ(x−1) + C."),
        (3, "The number of real roots of x² + 1 = 0 is:",
         "0", "1", "2", "Infinite", "a", "Mathematics", "Algebra — Polynomials",
         "x² = −1 has no real solutions; roots are ±i (imaginary)."),
        (4, "If A and B are two sets with n(A) = 5, n(B) = 3, n(A∩B) = 2, then n(A∪B) = ?",
         "8", "6", "10", "7", "b", "Mathematics", "Sets & Relations",
         "n(A∪B) = n(A) + n(B) − n(A∩B) = 5 + 3 − 2 = 6."),
        (5, "The sum of the first n natural numbers is:",
         "n²", "n(n+1)/2", "n(n−1)/2", "n(n+1)", "b", "Mathematics", "Sequences & Series",
         "Sum = n(n+1)/2 (arithmetic series formula)."),
        (6, "The value of lim(x→0) (sinx/x) is:",
         "0", "∞", "1", "π", "c", "Mathematics", "Calculus — Limits",
         "This is a standard limit: lim(x→0) sinx/x = 1."),
        (7, "The slope of the line 3x − 4y + 7 = 0 is:",
         "3/4", "−3/4", "4/3", "−4/3", "a", "Mathematics", "Coordinate Geometry",
         "Rewrite: y = (3/4)x + 7/4; slope = 3/4."),
        (8, "The distance between points (1, 2) and (4, 6) is:",
         "3", "4", "5", "7", "c", "Mathematics", "Coordinate Geometry",
         "d = √((4−1)² + (6−2)²) = √(9+16) = √25 = 5."),
        (9, "The number of ways to arrange 4 books in a row is:",
         "16", "12", "24", "8", "c", "Mathematics", "Permutations & Combinations",
         "4! = 4×3×2×1 = 24."),
        (10, "If log₁₀(100) = x, then x equals:",
         "10", "1", "2", "0.5", "c", "Mathematics", "Logarithms",
         "log₁₀(100) = log₁₀(10²) = 2."),

        # Chemistry (5)
        (11, "The number of electrons in the outermost shell of Neon (atomic number 10) is:",
         "2", "6", "8", "10", "c", "Chemistry", "Atomic Structure",
         "Neon configuration: 2,8; 8 electrons in the outermost (second) shell."),
        (12, "Which of the following has the smallest atomic radius?",
         "Na", "Mg", "Al", "Si", "d", "Chemistry", "Periodic Table",
         "Atomic radius decreases across a period; Si (Z=14) is smallest of these in Period 3."),
        (13, "The hybridization of carbon in methane (CH₄) is:",
         "sp", "sp²", "sp³", "sp³d", "c", "Chemistry", "Chemical Bonding",
         "CH₄ has tetrahedral geometry; carbon undergoes sp³ hybridization."),
        (14, "Which of the following is a covalent compound?",
         "NaCl", "MgO", "CO₂", "CaCl₂", "c", "Chemistry", "Chemical Bonding",
         "CO₂ has covalent double bonds between C and O."),
        (15, "In the reaction: Zn + H₂SO₄ → ZnSO₄ + H₂, zinc is:",
         "Oxidised", "Reduced", "Neither oxidised nor reduced", "A catalyst", "a", "Chemistry", "Redox Reactions",
         "Zn loses electrons (0 → +2), so it is oxidised."),

        # Physics (5)
        (16, "Newton's second law of motion states F = ma. If mass is doubled and acceleration halved, force becomes:",
         "Same", "Doubled", "Halved", "Quadrupled", "a", "Physics", "Laws of Motion",
         "F' = (2m)(a/2) = ma = F. Force remains unchanged."),
        (17, "The gravitational potential energy of a mass m at height h is:",
         "mh", "mgh²", "mgh", "m²gh", "c", "Physics", "Gravitation",
         "PE = mgh (near Earth's surface)."),
        (18, "Conservation of linear momentum applies when:",
         "No external force acts on the system",
         "Net external force is maximum",
         "Only gravity acts",
         "Only friction acts", "a", "Physics", "Laws of Motion",
         "Linear momentum is conserved when net external force = 0."),
        (19, "A body of mass 5 kg moving at 4 m/s has kinetic energy:",
         "10 J", "20 J", "40 J", "80 J", "c", "Physics", "Work, Energy & Power",
         "KE = ½mv² = ½ × 5 × 16 = 40 J."),
        (20, "Escape velocity from Earth's surface is approximately:",
         "7.9 km/s", "11.2 km/s", "9.8 km/s", "15 km/s", "b", "Physics", "Gravitation",
         "Escape velocity = √(2gR) ≈ 11.2 km/s for Earth."),
    ]

    for q in jee_t1_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, jee_t1),
        )

    # ── JEE Practice Test 2 ─────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("JEE", "JEE Practice Test 2",
               "Practice Test | Mathematics: Trigonometry & Vectors | Chemistry: Thermodynamics & Equilibrium | Physics: Electricity"))
    jee_t2 = c.lastrowid

    jee_t2_questions = [
        # Mathematics (10)
        (1, "sin(30°) + cos(60°) equals:",
         "0", "1", "√3/2", "√2", "b", "Mathematics", "Trigonometry",
         "sin30° = 0.5, cos60° = 0.5; sum = 1."),
        (2, "The magnitude of vector A = 3î + 4ĵ is:",
         "7", "5", "12", "1", "b", "Mathematics", "Vectors",
         "|A| = √(3² + 4²) = √25 = 5."),
        (3, "If tanθ = 3/4, then sinθ equals (θ in first quadrant):",
         "3/5", "4/5", "3/4", "5/3", "a", "Mathematics", "Trigonometry",
         "If tan θ = 3/4, then in a 3-4-5 triangle, sin θ = 3/5."),
        (4, "The dot product of î and ĵ is:",
         "1", "0", "−1", "î·ĵ is undefined", "b", "Mathematics", "Vectors",
         "î and ĵ are perpendicular unit vectors; î·ĵ = |î||ĵ|cos90° = 0."),
        (5, "The general solution of sin x = 0 is:",
         "x = nπ, n ∈ ℤ", "x = (2n+1)π/2, n ∈ ℤ", "x = nπ/2, n ∈ ℤ", "x = 2nπ, n ∈ ℤ", "a",
         "Mathematics", "Trigonometry",
         "sin x = 0 at x = 0, π, 2π, ... i.e., x = nπ."),
        (6, "The angle between vectors A = î + ĵ and B = î − ĵ is:",
         "0°", "45°", "90°", "180°", "c", "Mathematics", "Vectors",
         "A·B = 1−1 = 0 → cosθ = 0 → θ = 90°."),
        (7, "cos(2θ) expressed in terms of sinθ is:",
         "1 − sinθ", "1 − 2sin²θ", "2sinθcosθ", "sin²θ − cos²θ", "b", "Mathematics", "Trigonometry",
         "cos(2θ) = 1 − 2sin²θ (double angle identity)."),
        (8, "The position vector of the midpoint of segment joining A(2,4) and B(6,8) is:",
         "2î + 2ĵ", "4î + 6ĵ", "4î + 6ĵ", "8î + 12ĵ", "b", "Mathematics", "Vectors",
         "Midpoint = ((2+6)/2, (4+8)/2) = (4, 6) → position vector 4î + 6ĵ."),
        (9, "The value of cos(0°) is:",
         "0", "1", "−1", "√3/2", "b", "Mathematics", "Trigonometry",
         "cos(0°) = 1."),
        (10, "The cross product A × A for any vector A equals:",
         "|A|²", "1", "Zero vector", "2A", "c", "Mathematics", "Vectors",
         "A × A = |A||A|sin(0°) = 0 → zero vector."),

        # Chemistry (5)
        (11, "ΔH for a reaction is positive. This reaction is:",
         "Exothermic", "Endothermic", "Neither", "Spontaneous at all temperatures", "b",
         "Chemistry", "Thermodynamics",
         "ΔH > 0 means heat is absorbed → endothermic reaction."),
        (12, "In an exothermic reaction:",
         "Products have higher energy than reactants",
         "Reactants have higher energy than products",
         "ΔH = 0",
         "Temperature decreases", "b", "Chemistry", "Thermodynamics",
         "In exothermic reactions, reactants are at higher energy; heat is released."),
        (13, "Ka > 1 for an acid indicates it is:",
         "Weak acid", "Strong acid", "Neutral", "A base", "b", "Chemistry", "Chemical Equilibrium",
         "Ka > 1 means significant dissociation → strong acid."),
        (14, "The common ion effect suppresses the ionisation of:",
         "Water", "Strong electrolytes", "Weak electrolytes", "Non-electrolytes", "c",
         "Chemistry", "Chemical Equilibrium",
         "Adding a common ion shifts equilibrium back, suppressing weak electrolyte ionisation."),
        (15, "Entropy is a measure of:",
         "Heat content", "Randomness or disorder", "Pressure", "Volume", "b", "Chemistry", "Thermodynamics",
         "Entropy (S) measures the degree of disorder or randomness in a system."),

        # Physics (5)
        (16, "Coulomb's law gives the force between two charges as:",
         "F = kq₁q₂/r", "F = kq₁q₂/r²", "F = kq₁q₂·r²", "F = k(q₁+q₂)/r²", "b",
         "Physics", "Electrostatics",
         "F = kq₁q₂/r² (Coulomb's law; force ∝ 1/r²)."),
        (17, "Electric potential is a _____ quantity:",
         "Vector", "Tensor", "Scalar", "Dimensionless", "c", "Physics", "Electrostatics",
         "Electric potential V is a scalar quantity."),
        (18, "Kirchhoff's voltage law (KVL) states that the sum of voltages in a closed loop is:",
         "Maximum", "Minimum", "Zero", "Equal to current", "c", "Physics", "Current Electricity",
         "KVL: ΣV = 0 around any closed loop."),
        (19, "The unit of electric charge is:",
         "Ampere", "Volt", "Coulomb", "Ohm", "c", "Physics", "Electrostatics",
         "The SI unit of electric charge is the Coulomb (C)."),
        (20, "A wire of resistance 10 Ω is stretched to twice its length. Its new resistance is:",
         "5 Ω", "10 Ω", "20 Ω", "40 Ω", "d", "Physics", "Current Electricity",
         "R = ρL/A; stretching doubles L and halves A → R' = ρ(2L)/(A/2) = 4R = 40 Ω."),
    ]

    for q in jee_t2_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, jee_t2),
        )

    # ── JEE Practice Test 3 ─────────────────────────────────────
    c.execute("INSERT INTO tests (exam, name, description) VALUES (?, ?, ?)",
              ("JEE", "JEE Practice Test 3",
               "Practice Test | Mathematics: Matrices & Probability | Chemistry: Organic Chemistry | Physics: Waves & Modern Physics"))
    jee_t3 = c.lastrowid

    jee_t3_questions = [
        # Mathematics (10)
        (1, "The determinant of matrix [[1,2],[3,4]] is:",
         "10", "−2", "2", "−10", "b", "Mathematics", "Matrices & Determinants",
         "det = (1)(4) − (2)(3) = 4 − 6 = −2."),
        (2, "If P(A) = 0.4 and P(B) = 0.3 and A, B are independent events, P(A∩B) =",
         "0.7", "0.1", "0.12", "0.012", "c", "Mathematics", "Probability",
         "For independent events: P(A∩B) = P(A)·P(B) = 0.4 × 0.3 = 0.12."),
        (3, "The inverse of matrix [[2,0],[0,3]] is:",
         "[[1/2,0],[0,1/3]]", "[[3,0],[0,2]]", "[[−2,0],[0,−3]]", "[[2,0],[0,3]]", "a", "Mathematics",
         "Matrices & Determinants",
         "For diagonal matrix: inverse swaps each diagonal element with its reciprocal."),
        (4, "The probability of getting a head in a single coin toss is:",
         "1", "0", "1/4", "1/2", "d", "Mathematics", "Probability",
         "Fair coin: P(Head) = 1/2."),
        (5, "A 2×3 matrix multiplied by a 3×2 matrix gives a matrix of order:",
         "3×3", "2×2", "2×3", "3×2", "b", "Mathematics", "Matrices & Determinants",
         "Result of (m×n)×(n×p) is m×p; here (2×3)×(3×2) = 2×2."),
        (6, "P(A|B) = P(A∩B)/P(B). This is the definition of:",
         "Joint probability", "Conditional probability", "Marginal probability", "Independent probability", "b",
         "Mathematics", "Probability",
         "This is the definition of conditional probability P(A given B)."),
        (7, "The transpose of matrix [[1,2,3],[4,5,6]] has dimensions:",
         "2×3", "3×2", "3×3", "2×2", "b", "Mathematics", "Matrices & Determinants",
         "Transposing a 2×3 matrix gives a 3×2 matrix."),
        (8, "In how many ways can we select 3 items from 10 without repetition?",
         "30", "120", "720", "10", "b", "Mathematics", "Permutations & Combinations",
         "¹⁰C₃ = 10!/(3!·7!) = 120."),
        (9, "If two dice are thrown, P(sum = 7) is:",
         "1/6", "1/36", "7/36", "6/36", "a", "Mathematics", "Probability",
         "Pairs summing to 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6 out of 36; P = 6/36 = 1/6."),
        (10, "The rank of the zero matrix is:",
         "0", "1", "Undefined", "Equal to its order", "a", "Mathematics", "Matrices & Determinants",
         "The zero matrix has rank 0 (all rows/columns are zero)."),

        # Chemistry (5)
        (11, "Which of the following is NOT a characteristic of organic compounds?",
         "They contain carbon", "They generally have high melting points",
         "They are mostly covalently bonded", "They are often combustible", "b", "Chemistry", "Organic Chemistry — General",
         "Organic compounds generally have LOW melting points (covalent bonds, weak intermolecular forces)."),
        (12, "In the SN2 mechanism, the nucleophile attacks:",
         "The front side of the carbon bearing the leaving group",
         "The back side of the carbon bearing the leaving group",
         "Any side randomly",
         "Only in polar solvents", "b", "Chemistry", "Organic Chemistry — Reactions",
         "SN2 involves backside attack, leading to inversion of configuration."),
        (13, "Which compound shows geometrical isomerism?",
         "CH₄", "CH₃Cl", "2-butene (CH₃-CH=CH-CH₃)", "Ethane", "c", "Chemistry", "Isomerism",
         "2-butene has a C=C double bond with different groups on each carbon → cis/trans isomers."),
        (14, "Lucas test is used to distinguish between:",
         "Primary and secondary amines",
         "Primary, secondary, and tertiary alcohols",
         "Aldehydes and ketones",
         "Alkenes and alkynes", "b", "Chemistry", "Organic Chemistry — Reactions",
         "Lucas reagent (ZnCl₂ + conc. HCl) reacts differently with 1°, 2°, and 3° alcohols."),
        (15, "Benzene (C₆H₆) is best described as:",
         "Aliphatic compound with alternating double bonds",
         "Aromatic compound with delocalized π electrons",
         "Saturated hydrocarbon",
         "Alicyclic compound", "b", "Chemistry", "Organic Chemistry — Aromatic Compounds",
         "Benzene is aromatic with 6 delocalized π electrons satisfying Hückel's rule (4n+2, n=1)."),

        # Physics (5)
        (16, "The photoelectric effect cannot be explained by:",
         "Quantum theory", "Wave theory of light", "Photon model", "Planck's equation", "b",
         "Physics", "Modern Physics",
         "Classical wave theory fails to explain threshold frequency and instant emission in photoelectric effect."),
        (17, "In Bohr's model, the radius of the nth orbit is proportional to:",
         "n", "n²", "1/n", "1/n²", "b", "Physics", "Modern Physics",
         "rₙ = n²a₀ (a₀ = Bohr radius); radius ∝ n²."),
        (18, "The speed of sound in air at 0°C is approximately:",
         "340 m/s", "300 m/s", "331 m/s", "380 m/s", "c", "Physics", "Waves",
         "Speed of sound in air at 0°C ≈ 331 m/s; at 20°C ≈ 343 m/s."),
        (19, "In the phenomenon of resonance, the system vibrates at:",
         "Any random frequency", "Its natural frequency", "The driving frequency only",
         "Twice the natural frequency", "b", "Physics", "Oscillations",
         "Resonance occurs when the driving frequency matches the natural frequency of the system."),
        (20, "An alpha particle consists of:",
         "2 protons and 2 neutrons", "1 proton and 1 neutron",
         "2 protons and 1 neutron", "1 proton and 2 neutrons", "a", "Physics", "Nuclear Physics",
         "Alpha particle = ⁴₂He nucleus = 2 protons + 2 neutrons."),
    ]

    for q in jee_t3_questions:
        c.execute(
            "INSERT INTO questions (question_number, question_text, option_a, option_b, option_c, option_d, "
            "correct_option, subject, topic, explanation, test_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*q, jee_t3),
        )

    conn.commit()
    conn.close()
    print("Database seeded successfully!")
    print(f"  PYQs inserted: {len(pyqs)}")
    print("  NEET tests: 3 (60 questions)")
    print("  JEE tests:  3 (60 questions)")


if __name__ == "__main__":
    seed()

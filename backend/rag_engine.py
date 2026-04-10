import os
from manual_loader import search_manuals


# Gemini optional support
try:
    import google.genai as genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


# =============================
# CONFIDENCE ENGINE
# =============================

def calculate_confidence(issue, solution, source):

    score = 0

    # -------------------------
    # FEATURE 1: SOURCE WEIGHT
    # -------------------------
    source_weight = {
        "manual": 0.50,
        "ai": 0.30,
        "none": 0.10
    }

    score += source_weight.get(source, 0.20)


    # -------------------------
    # FEATURE 2: KEYWORD MATCH SCORE
    # -------------------------
    issue_words = set(issue.lower().split())
    solution_words = set(solution.lower().split())

    if len(issue_words) > 0:

        keyword_overlap = len(issue_words & solution_words) / len(issue_words)

        score += keyword_overlap * 0.25


    # -------------------------
    # FEATURE 3: DEVICE DETECTION BONUS
    # -------------------------
    device = extract_device(solution)

    if device != "UNKNOWN DEVICE":

        score += 0.15


    # -------------------------
    # FEATURE 4: SOLUTION COMPLETENESS
    # -------------------------
    solution_length = len(solution.split())

    if solution_length > 120:

        score += 0.10

    elif solution_length > 50:

        score += 0.05


    # -------------------------
    # FINAL NORMALIZATION
    # -------------------------
    confidence_percent = int(min(score * 100, 95))

    return confidence_percent


# =============================
# DEVICE DETECTION ENGINE
# =============================

def extract_device(solution_text):

    for line in solution_text.split("\n"):

        if "DEVICE:" in line.upper():

            return line.replace("DEVICE:", "").strip()

    return "UNKNOWN DEVICE"


# =============================
# RESPONSE FORMATTER
# =============================

def format_response(issue, solution, source):

   confidence = calculate_confidence(issue, solution, source)

    device = extract_device(solution)

    return {

        "device": device,
        "issue": issue.upper(),
        "solution": solution,
        "confidence": confidence,
        "source": source

    }


# =============================
# MAIN RAG PIPELINE
# =============================

def ask_resolvex(question):

    question = question.strip().lower()

    print(f"[ResolveX] Processing query: {question}")


    # STEP 1 — SEARCH MANUAL DATABASE

    manual_answer = search_manuals(question)

    if manual_answer:

        return format_response(
            issue=question,
            solution=manual_answer,
            source="manual"
        )


    # STEP 2 — GEMINI FALLBACK MODE

    if GEMINI_AVAILABLE:

        try:

            client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

            prompt = f"""
You are ResolveX Intelligence,
a biomedical troubleshooting assistant.

Provide structured engineering troubleshooting steps
for the following issue:

{question}

Return clear step-by-step solution.
"""

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            ai_solution = response.text.strip()

            return format_response(
                issue=question,
                solution=ai_solution,
                source="ai"
            )

        except Exception as e:

            print("[ResolveX Gemini Error]", e)


    # STEP 3 — FAILURE MODE

    return format_response(
        issue=question,
        solution="""
DEVICE: UNKNOWN DEVICE

No troubleshooting steps found in manual database.

Recommendation:
Upload device service manual
or enable AI reasoning mode.
""",
        source="none"
    )

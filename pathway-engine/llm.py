# llm.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import ingestions

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def build_context() -> str:
    """
    Builds a STRICT factual context so LLM cannot hallucinate counts.
    """
    a = len(ingestions.assignments)
    e = len(ingestions.exams)
    v = len(ingestions.events)

    lines = [
        "FACTS (DO NOT INVENT DATA):",
        f"Assignments count: {a}",
        f"Exams count: {e}",
        f"Events count: {v}",
        "",
    ]

    if a:
        lines.append("Assignments:")
        for x in ingestions.assignments:
            lines.append(f"- {x['title']} (due in {x['due_in_days']} days)")
        lines.append("")

    if e:
        lines.append("Exams:")
        for x in ingestions.exams:
            lines.append(f"- {x['title']} (in {x['due_in_days']} days)")
        lines.append("")

    if v:
        lines.append("Events:")
        for x in ingestions.events:
            lines.append(f"- {x['title']} (in {x['due_in_days']} days)")
        lines.append("")

    return "\n".join(lines)


def ask_llm(context: str, question: str) -> str:
    prompt = f"""
You are a calm, supportive student productivity assistant.

If the user asks for planning, provide:
1) Today plan
2) Next 7-day plan
3) What can wait

RULES:
- Use workload analysis strictly
- Focus on next 7 days
- Provide actionable steps
- Do not invent deadlines

{context}

User question:
{question}
"""

    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"LLM error: {e}"

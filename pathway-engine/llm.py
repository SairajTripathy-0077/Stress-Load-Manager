import os
from dotenv import load_dotenv
import google.generativeai as genai
import ingestions

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash") # Use stable model name

def build_context() -> str:
    """Creates a detailed factual string for the AI using the latest memory state."""
    # Ensure memory is fresh before building
    ingestions.refresh_from_disk()
    
    a, e, v = ingestions.assignments, ingestions.exams, ingestions.events
    
    lines = [
        "FACTS (DO NOT HALLUCINATE):",
        f"Total Assignments: {len(a)}",
        f"Total Exams: {len(e)}",
        f"Total Events: {len(v)}",
        "\nDETAILS:"
    ]

    # Add specific titles so the AI can actually plan for them
    for item in a: lines.append(f"- Assignment: {item['title']} (Due: {item['due_in_days']} days)")
    for item in e: lines.append(f"- Exam: {item['title']} (In: {item['due_in_days']} days)")
    for item in v: lines.append(f"- Event: {item['title']} (In: {item['due_in_days']} days)")

    return "\n".join(lines)

def ask_llm(context: str, question: str) -> str:
    """Sends the context and question to Gemini with strict behavioral instructions."""
    prompt = f"""
    You are a supportive student productivity assistant. 
    Using the facts below, create a short 1) Today Plan, 2) 7-Day Plan, 3) Priorities.
    
    RULES:
    - Only use the data provided.
    - Do not use markdown symbols like * or #.
    - Keep it concise.

    {context}

    User Question: {question}
    """
    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"AI Service Error: {str(e)}"
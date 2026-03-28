from google import genai
import os
from core.prompt import SYSTEM_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_jarvis(user_input, history=None, lang="en"):
    if history is None:
        history = []

    system_prompt = SYSTEM_PROMPT
    if lang == "hi":
        system_prompt += "\nRespond in Hindi."
    else:
        system_prompt += "\nRespond in English."

    contents = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        *history,
        {"role": "user", "parts": [{"text": user_input}]}
    ]

    try:
        response = client.models.generate_content(
            model="gemini-1.0-pro",  # ✅ WORKING
            contents=contents
        )
        reply = response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        reply = " Sir I'm currently unavailable."

    history.append({"role": "user", "parts": [{"text": user_input}]})
    history.append({"role": "model", "parts": [{"text": reply}]})

    return reply, history

from google import genai
import os
from core.prompt import SYSTEM_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_jarvis(user_input, history=None, lang="en"):
    if history is None:
        history = []

    system_prompt = SYSTEM_PROMPT + "\nRespond primarily in professional English. However, if the user speaks entirely in Hindi, you may respond in Hindi to maintain a natural flow. For mixed language (Hinglish) or technical commands, always stick to English."
    if lang == "hi":
        system_prompt += "\nThe user spoke in Hindi; you may reply in Hindi if appropriate."
    else:
        system_prompt += "\nStick to professional English."


    contents = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        *history,
        {"role": "user", "parts": [{"text": user_input}]}
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Updated to the new generation model
            contents=contents
        )
        reply = response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        reply = " Sir I'm currently unavailable."

    history.append({"role": "user", "parts": [{"text": user_input}]})
    history.append({"role": "model", "parts": [{"text": reply}]})

    return reply, history

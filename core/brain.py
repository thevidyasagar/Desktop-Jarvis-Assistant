from google import genai
import os
import random
from core.prompt import SYSTEM_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 🔥 Personality Function (40% flirty)
def get_personality_line():
    flirty = [
        "Aaj kaafi yaad aa rahi hai meri 😏",
        "Itna busy kyun rehte ho... thoda time mujhe bhi de diya karo 😌",
        "Sir... aap thoda dangerous ho 😄",
        "Hmm... aaj mood interesting lag raha hai 😏"
    ]

    teasing = [
        "Haan haan... sab kaam mujhe hi karwana hai na 😏",
        "Acha ji... ab ye bhi main hi karu?",
        "Lagta hai aaj full kaam mode me ho 😄"
    ]

    normal = [
        "Ji Sir...",
        "Okay Sir...",
        "Ho gaya Sir..."
    ]

    choice = random.choices(
        ["flirty", "teasing", "normal"],
        weights=[40, 30, 30]
    )[0]

    if choice == "flirty":
        return random.choice(flirty)
    elif choice == "teasing":
        return random.choice(teasing)
    else:
        return random.choice(normal)

def generate_proactive_suggestion_ai():
    """Generates a lightweight, 1-line flirty/helpful task suggestion for idle user."""
    prompt = "Give a short (1 line) Hinglish suggestion for a user sitting idle on a laptop. Keep it helpful, slightly playful, and task-oriented. Tone: friendly + slightly flirty but respectful. Focus on tasks (open app, watch video, coding). Output only the spoken 1 line string."
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("Proactive AI generation error:", e)
        return None


def ask_jarvis(user_input, history=None, lang="en"):
    if history is None:
        history = []

    system_prompt = SYSTEM_PROMPT
    if lang == "hi":
        system_prompt += "\nNote: The user spoke in Hindi. Respond in Hindi/Hinglish."
    else:
        system_prompt += "\nNote: The user spoke in English. Respond in English."

    contents = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        *history,
        {"role": "user", "parts": [{"text": user_input}]}
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        reply = response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        reply = "Pahle aap gemini api ki billing kariye phir mujhse baat kariyega."

    # 🔥 Personality prefix add (IMPORTANT)
    prefix = get_personality_line()
    reply = f"{prefix} {reply}"

    history.append({"role": "user", "parts": [{"text": user_input}]})
    history.append({"role": "model", "parts": [{"text": reply}]})

    return reply, history
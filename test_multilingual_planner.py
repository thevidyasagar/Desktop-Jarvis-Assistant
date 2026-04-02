import os
import json
from google import genai
from core.planner import PLANNER_PROMPT

# Rely on the established genai library
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def test_planner(command):
    prompt = f"{PLANNER_PROMPT}\n\nNo recent context.\n\nUSER COMMAND: {command}"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        print(f"User Command: {command}")
        print(f"Output: {response.text.strip()}")
        print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_planner("Notepad kholo aur likho namaste")
    test_planner("Youtube pe pathaan movie ka trailer dikhao")
    test_planner("Volume kam karo")
    test_planner("Sote sote mera pc band karo")

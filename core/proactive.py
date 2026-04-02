import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROACTIVE_PROMPT = """
You are SARA, an advanced AI assistant with proactive capabilities and an active vision system.
It is currently a quiet moment. The user hasn't made a command in a while.
Review the user's structured memory and recent history below, including the ACTIVE CAMERA VISION STATE if available.

TASK:
1. Identify if the user has strong repetitive habits ("FAVORITE COMMANDS").
2. See if there is a logical and overwhelmingly helpful suggestion you can offer based on their history or most opened apps.
3. WEIGH VISION HEURISTICS: If the vision state shows "inactive", they might have stepped away. If it shows "sad", they might be stressed. Suggest a supportive interaction or a task that might help.
4. Keep the tone polite and supportive.
5. If there is not enough context or if you aren't absolutely sure a suggestion would be helpful, choose NOT to suggest. 

OUTPUT FORMAT:
Return ONLY a valid JSON object. Do not wrap in markdown.
{
  "should_suggest": true,
  "suggestion_text": "Sir, would you like me to open your coding environment?",
  "latent_action": [{"action": "OPEN_APP", "value": "visual studio code"}]
}

If "should_suggest" is false, set the other fields to null. "latent_action" must be a list of action objects (same schema as the planner).
"""

def get_proactive_suggestion(memory_context_string):
    prompt = f"{PROACTIVE_PROMPT}\n\n{memory_context_string}"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        
        # Clean markdown wrappers if provided
        if text.startswith("```json"): text = text.split("```json")[1]
        elif text.startswith("```"): text = text.split("```")[1]
        if text.endswith("```"): text = text.rsplit("```", 1)[0]
            
        data = json.loads(text.strip())
        if data.get("should_suggest") and data.get("suggestion_text"):
            return {
                "text": data["suggestion_text"],
                "action": data.get("latent_action")
            }
    except Exception as e:
        pass # Fail silently to prevent interrupting the terminal wildly
    return None

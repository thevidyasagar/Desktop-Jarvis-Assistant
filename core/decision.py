from core.intent import detect_intent
import re

def decide_action(text):
    intent = detect_intent(text)
    
    action_dict = {
        "action": "NONE",
        "value": None
    }
    
    if intent == "UNKNOWN":
        return action_dict

    # 🌐 App Open Logic
    if intent == "OPEN_APP":
        # Extract everything after the open word
        words = text.split()
        target = ""
        for i, w in enumerate(words):
            if w in ["open", "start", "launch", "chalao"] and i + 1 < len(words):
                target = " ".join(words[i+1:])
                break
        
        if "youtube" in target:
            action_dict["action"] = "OPEN_URL"
            action_dict["value"] = "https://www.youtube.com"
        elif "google" in target:
            action_dict["action"] = "OPEN_URL"
            action_dict["value"] = "https://www.google.com"
        elif "facebook" in target:
            action_dict["action"] = "OPEN_URL"
            action_dict["value"] = "https://www.facebook.com"
        else:
            action_dict["action"] = "OPEN_APP"
            action_dict["value"] = target.replace(" ", "") # E.g. "notepad", "calculator"

    # 🌐 Web Search Logic
    elif intent in ["GOOGLE_SEARCH", "YOUTUBE_SEARCH", "WIKIPEDIA_SEARCH", "AMAZON_SEARCH", "DUCKDUCKGO_SEARCH", "STACKOVERFLOW_SEARCH"]:
        query = text
        # Remove trigger phrases to isolate the actual search query
        triggers = [
            "open google and search for", "open google and search",
            "open youtube and search for", "open youtube and search",
            "search on google for", "search google for", "google search", 
            "search on youtube for", "search youtube for", "youtube search", "youtube pe search",
            "search on wikipedia for", "search wikipedia for", "wikipedia search",
            "search on duckduckgo for", "search duckduckgo for", "duckduckgo search",
            "search on amazon for", "search amazon for", "amazon search",
            "search on stack overflow for", "search stack overflow for", 
            "search stackoverflow for", "search for", "search", "look for", "find"
        ]
        
        for trigger in triggers:
            if trigger in query:
                # Split and take everything after the first match of the trigger
                query = query.split(trigger, 1)[-1].strip()
                break
                
        # Clean trailing platforms for queries like "cats on youtube"
        query = re.sub(r' (on|in) (google|youtube|wikipedia|amazon|duckduckgo|stack overflow|stackoverflow)$', '', query, flags=re.IGNORECASE).strip()
        
        action_dict["action"] = intent
        action_dict["value"] = query

    # 🖥️ System App Actions (No value needed)
    elif intent in ["VOLUME_UP", "VOLUME_DOWN", "VOLUME_MUTE", "SCREENSHOT", "SYSTEM_SLEEP", "SYSTEM_RESTART", "SYSTEM_SHUTDOWN", "MEDIA_PLAY_PAUSE", "MEDIA_NEXT", "MEDIA_PREV", "MINIMIZE_ALL", "CLOSE_CURRENT_WINDOW"]:
        action_dict["action"] = intent

    return action_dict

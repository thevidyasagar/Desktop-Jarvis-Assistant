# core/decision.py

def decide_action(intent, app):
    if intent == "OPEN_APP" and app:

        # 🌐 Browser based apps
        if app == "youtube":
            return {
                "action": "OPEN_URL",
                "value": "https://www.youtube.com"
            }

        # 🖥️ System apps
        if app in ["notepad", "calculator", "cmd", "chrome"]:
            return {
                "action": "OPEN_APP",
                "value": app
            }

    return {
        "action": "NONE",
        "value": None
    }

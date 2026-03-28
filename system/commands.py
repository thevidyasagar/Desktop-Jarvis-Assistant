from system.app_launcher import open_app

def handle_system_command(text):
    text = text.lower()

    # open any app
    if "open" in text or "start" in text or "launch" in text:
        words = text.replace("open", "").replace("start", "").replace("launch", "").strip()
        reply = open_app(words)
        if reply:
            return reply

    return None

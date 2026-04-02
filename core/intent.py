def detect_intent(text):
    text = text.lower()

    # Handle Web Searches first or they might get caught by OPEN_APP if user says "open google and search"
    if any(k in text for k in ["search", "find", "look for", "dhoondho"]):
        if "youtube" in text:
            return "YOUTUBE_SEARCH"
        elif "wikipedia" in text:
            return "WIKIPEDIA_SEARCH"
        elif "amazon" in text:
            return "AMAZON_SEARCH"
        elif "duckduckgo" in text:
            return "DUCKDUCKGO_SEARCH"
        elif "stack overflow" in text or "stackoverflow" in text:
            return "STACKOVERFLOW_SEARCH"
        else:
            return "GOOGLE_SEARCH"
            
    if any(k in text for k in ["open", "kholo", "start", "launch", "chalao"]):
        return "OPEN_APP"

    if any(k in text for k in ["close", "band", "exit"]):
        return "CLOSE_APP"

    if any(k in text for k in ["type", "likho", "write"]):
        return "TYPE_TEXT"

    if any(k in text for k in ["volume up", "louder", "increase volume", "volume bdhaw"]):
        return "VOLUME_UP"
    if any(k in text for k in ["volume down", "quieter", "decrease volume", "lower volume", "volume kam"]):
        return "VOLUME_DOWN"
    if any(k in text for k in ["mute", "shut up", "silence"]):
        return "VOLUME_MUTE"
        
    if any(k in text for k in ["screenshot", "screen shot", "capture screen"]):
        return "SCREENSHOT"
        
    if any(k in text for k in ["sleep", "lock screen", "sleep model"]):
        return "SYSTEM_SLEEP"
    if any(k in text for k in ["restart", "reboot", "restart computer"]):
        return "SYSTEM_RESTART"
    # Note: shutdown is also handled in main.py, but we capture the intent here for formal decision making
    if any(k in text for k in ["shutdown", "shut down", "turn off computer"]):
        return "SYSTEM_SHUTDOWN"
        
    if any(k in text for k in ["play music", "pause music", "stop music", "play video", "pause video", "play media", "pause media"]):
        return "MEDIA_PLAY_PAUSE"
    if any(k in text for k in ["next song", "next track", "skip song"]):
        return "MEDIA_NEXT"
    if any(k in text for k in ["previous song", "previous track", "last song"]):
        return "MEDIA_PREV"
        
    if any(k in text for k in ["minimize", "show desktop", "hide windows"]):
        return "MINIMIZE_ALL"
    if any(k in text for k in ["close window", "close current window"]):
        return "CLOSE_CURRENT_WINDOW"

    return "UNKNOWN"

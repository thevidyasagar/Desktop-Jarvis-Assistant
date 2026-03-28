def detect_intent(text):
    text = text.lower()

    if any(k in text for k in ["open", "kholo", "start", "launch", "chalao"]):
        return "OPEN_APP"

    if any(k in text for k in ["close", "band", "exit"]):
        return "CLOSE_APP"

    if any(k in text for k in ["type", "likho", "write"]):
        return "TYPE_TEXT"

    return "UNKNOWN"

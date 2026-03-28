def get_response_language(text, whisper_lang):
    text_lower = text.lower()

    # 1️⃣ Explicit instruction (highest priority)
    if "english me" in text_lower or "english mein" in text_lower:
        return "english"

    if "hindi me" in text_lower or "hindi mein" in text_lower:
        return "hindi"

    # 2️⃣ Whisper detected language (most reliable)
    if whisper_lang == "hi":
        return "hindi"

    return "english"

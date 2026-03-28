# core/entity.py

import re

APP_KEYWORDS = {
    "youtube": [
        "youtube", "you tube", "your tube", "u tube", "utube", "youtub"
    ],
    "notepad": [
        "notepad", "note pad", "nodepad", "note ped"
    ],
    "chrome": [
        "chrome", "google chrome", "chrom"
    ],
    "calculator": [
        "calculator", "calc", "calci", "calculater"
    ],
    "cmd": [
        "command prompt", "cmd", "terminal", "command"
    ],
    "whatsapp": [
        "whatsapp", "what's app", "what app", "watsapp", "whatsap"
    ],
    "settings": [
        "settings", "system settings", "windows settings"
    ]
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_app_name(text: str):
    if not text:
        return None

    text = normalize_text(text)

    # direct keyword match
    for app, keywords in APP_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return app

    return None

import re
import time
from voice.listen import listen
from voice.speak import speak
# ... (Other imports same rahenge)

WAKE_PATTERNS = ["joya", "jo ya", "jaya", "zoya", "hey joya"]

def is_wake_word(text: str) -> bool:
    text = re.sub(r"[^\w\s]", "", text.lower()).strip()
    return any(p in text for p in WAKE_PATTERNS)

def start_veda():
    print("🟢 Joya Online")
    speak("Hello Boss. Joya is ready for you. kya hukum hai sir?")
    
    conversation = []

    while True:
        text, _ = listen()
        if not text: continue

        if is_wake_word(text):
            speak("Yes Sir?") # Quick response
            
            command, lang = listen() # Listen for actual command
            if not command: continue
            
            user_text = command.lower()
            print(f"🎯 Command: {user_text}")

            # Exit Logic
            if any(w in user_text for w in ["shutdown", "exit", "bye"]):
                speak("Goodbye Sir. System offline.")
                break

            # Intent & Action Logic (Same as yours)
            # ... [Your Detect Intent / Execute Action code here] ...

            # Fallback to AI
            reply, conversation = ask_jarvis(user_text, conversation, lang)
            speak(reply)

if __name__ == "__main__":
    start_veda()
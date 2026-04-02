# from ui.jarvis_ui import start_ui

# start_ui()


from voice.listen import listen
from voice.speak import speak
import time

print("Sara test started")
speak("Sara test started. Speak anything.")

while True:
    text, lang = listen()

    if not text or not text.strip():
        time.sleep(0.3)
        continue

    print("Heard:", text, "| Lang:", lang)

    speak("I heard you")

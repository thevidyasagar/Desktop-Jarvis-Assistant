import os
import webbrowser
import subprocess
import time
import smtplib
import pyautogui
from email.mime.text import MIMEText

# Try importing the new modules, gracefully degrading if not available yet
try:
    from actions.system import volume_control, media_control, window_control, take_screenshot, system_power
    from actions.web import google_search, youtube_search, wikipedia_search, amazon_search, duckduckgo_search, stackoverflow_search
except ImportError as e:
    print("Action Import Error:", e)

# =========================
# 🔹 APP / SYSTEM ACTIONS
# =========================

def open_app(app_name):
    try:
        app_name = app_name.lower()
        if app_name == "notepad":
            subprocess.Popen(["notepad.exe"])
        elif app_name == "calculator" or app_name == "calc":
            subprocess.Popen(["calc.exe"])
        elif app_name == "cmd" or app_name == "commandprompt":
            subprocess.Popen(["cmd.exe"])
        elif app_name == "chrome":
            # Just launching chrome might need path, or try os.system
            os.system("start chrome")
        else:
            return "App unhandled or unrecognized."
        return f"Opened {app_name}."

    except Exception as e:
        print("Open app error:", e)
        return "Failed to open application."


def open_url(url):
    try:
        webbrowser.open(url)
        return "Opening URL."
    except Exception as e:
        print("Open url error:", e)
        return "Failed to open URL."


# =========================
# 🔹 WhatsApp & Email (Original logic retained)
# =========================
def send_whatsapp_by_name(name, message):
    try:
        subprocess.Popen("whatsapp:")
        time.sleep(6)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(name, interval=0.1)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write(message, interval=0.05)
        pyautogui.press("enter")
        return "WhatsApp message sent."
    except Exception as e:
        print("WhatsApp error:", e)
        return "Failed to send WhatsApp message."

def send_email(to_email, subject, body):
    return "Email functionality currently mocked/disabled."

# =========================
# 🔹 MASTER EXECUTOR
# =========================

def execute_action(action_dict):
    """Executes the mapped action dictionary and returns spoken confirmation string."""
    action = action_dict.get("action")
    value = action_dict.get("value")

    if action == "NONE" or action == "UNKNOWN":
        return None

    print(f"Executing: {action} -> {value}")

    if action == "OPEN_APP":
        return open_app(value)
    if action == "OPEN_URL":
        return open_url(value)
    if action == "GOOGLE_SEARCH":
        return google_search(value)
    if action == "YOUTUBE_SEARCH":
        return youtube_search(value)
    if action == "WIKIPEDIA_SEARCH":
        return wikipedia_search(value)
    if action == "AMAZON_SEARCH":
        return amazon_search(value)
    if action == "DUCKDUCKGO_SEARCH":
        return duckduckgo_search(value)
    if action == "STACKOVERFLOW_SEARCH":
        return stackoverflow_search(value)
        
    if action == "TYPE_TEXT" and value:
        # Safety Fail-Safe: Moving mouse to any corner of the screen stops the procedure
        pyautogui.FAILSAFE = True
        
        # Give a generous delay for the app window to focus (e.g. after OPEN_APP)
        # In a real scenario, we could use pyautogui.getWindowsWithTitle(value) 
        # but let's stick to a robust delay and a safe click to ensure focus.
        print("⏳ Preparing to type... Move mouse to a corner to STOP.")
        time.sleep(2.0)
        
        # Typing with a safe interval to ensure the application registers all characters
        # especially for complex code with indentation.
        pyautogui.write(value, interval=0.01)
        return "Finished typing. (Failsafe active: move mouse to corner to interrupt)"

    if action in ["VOLUME_UP", "VOLUME_DOWN", "VOLUME_MUTE"]:
        return volume_control(action.split("_")[-1]) # UP, DOWN, MUTE
        
    if action in ["MEDIA_PLAY_PAUSE", "MEDIA_NEXT", "MEDIA_PREV"]:
        return media_control(action.replace("MEDIA_", ""))
        
    if action in ["MINIMIZE_ALL", "CLOSE_CURRENT_WINDOW"]:
        if action == "CLOSE_CURRENT_WINDOW": return window_control("CLOSE_CURRENT")
        return window_control(action)
        
    if action == "SCREENSHOT":
        return take_screenshot()
        
    if action in ["SYSTEM_SLEEP", "SYSTEM_RESTART", "SYSTEM_SHUTDOWN"]:
        # handled manually or executed directly
        return system_power(action.replace("SYSTEM_", ""))

    if action == "SEND_WHATSAPP_NAME":
        return send_whatsapp_by_name(value["name"], value["message"])
    if action == "SEND_EMAIL":
        return send_email(value["to"], value["subject"], value["body"])

    return None

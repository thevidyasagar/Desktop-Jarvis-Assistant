import os
import webbrowser
import subprocess
import time
import smtplib
import pyautogui
from email.mime.text import MIMEText

# Try importing the new modules, gracefully degrading if not available yet
try:
    from actions.system import volume_control, media_control, window_control, take_screenshot, system_power, get_system_stats, set_brightness, toggle_wifi, system_optimize
    from actions.web import google_search, youtube_search, wikipedia_search, amazon_search, duckduckgo_search, stackoverflow_search
    from actions.developer import create_project, write_file, execute_code, open_vscode
    from actions.files import smart_search, open_file_safe, delete_to_recycle_bin, rename_file, create_directory
except ImportError as e:
    print("Action Import Error:", e)

# =========================
# 🔹 APP / SYSTEM ACTIONS
# =========================

def open_app(app_name):
    try:
        if ":" in app_name: # Handle specialized app targets like vscode:project
            tag, project = app_name.split(":", 1)
            if tag == "vscode" or tag == "code":
                return open_vscode(project)
                
        if app_name == "notepad":
            subprocess.Popen(["notepad.exe"])
        elif app_name == "calculator" or app_name == "calc":
            subprocess.Popen(["calc.exe"])
        elif app_name == "cmd" or app_name == "commandprompt":
            subprocess.Popen(["cmd.exe"])
        elif app_name == "chrome":
            os.system("start chrome")
        elif app_name == "vscode" or app_name == "code":
            subprocess.Popen(["code", "."], shell=True)
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

    if action == "CREATE_PROJECT":
        return create_project(value)
    if action == "WRITE_FILE" and isinstance(value, dict):
        return write_file(value["project"], value["path"], value["content"])
    if action == "RUN_CODE" and isinstance(value, dict):
        return execute_code(value["project"], value["path"])

    if action == "RENAME_FILE" and isinstance(value, dict):
        return rename_file(value["path"], value["new_name"])
    if action == "DELETE_FILE":
        return delete_to_recycle_bin(value)
    if action == "CREATE_DIR":
        if isinstance(value, dict): return create_directory(value["name"], value.get("parent"))
        return create_directory(value)
    if action == "OPEN_FILE":
        return open_file_safe(value)

    if action == "SYSTEM_INFO":
        return get_system_stats()
    if action == "SET_SYSTEM" and isinstance(value, dict):
        if value["type"] == "brightness": return set_brightness(value["value"])
        if value["type"] == "wifi": return toggle_wifi(value["value"])
    if action == "OPTIMIZE":
        return system_optimize()
    if action == "HOTKEY" and isinstance(value, list):
        pyautogui.hotkey(*value)
        return f"Executing hotkey: {'+'.join(value)}"

    if action == "CLICK_AT" and value:
        x, y = value.get("x"), value.get("y")
        pyautogui.click(x, y)
        return f"Clicked at {x}, {y}."

    if action == "SCROLL" and value:
        direction = str(value).lower()
        if direction == "down": pyautogui.scroll(-500)
        elif direction == "up": pyautogui.scroll(500)
        return f"Scrolled {direction}."

    return None

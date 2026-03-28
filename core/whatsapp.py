import time
import subprocess
import pyautogui


def send_whatsapp_by_name(name, message):
    try:
        # Open WhatsApp Desktop
        subprocess.Popen("whatsapp:")
        time.sleep(6)  # app load hone ka wait

        # Focus search
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)

        # Type contact name
        pyautogui.write(name, interval=0.1)
        time.sleep(2)

        # Open chat
        pyautogui.press("enter")
        time.sleep(1)

        # Type message
        pyautogui.write(message, interval=0.05)
        pyautogui.press("enter")

        return True

    except Exception as e:
        print("WhatsApp error:", e)
        return False

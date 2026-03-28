import os
import webbrowser
import subprocess
import time
import smtplib
import pyautogui

from email.mime.text import MIMEText


# =========================
# 🔹 APP / SYSTEM ACTIONS
# =========================

def open_app(app_name):
    try:
        if app_name == "notepad":
            subprocess.Popen(["notepad.exe"])

        elif app_name == "calculator":
            subprocess.Popen(["calc.exe"])

        elif app_name == "cmd":
            subprocess.Popen(["cmd.exe"])

        else:
            return False

        return True

    except Exception as e:
        print("Open app error:", e)
        return False


def open_url(url):
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print("Open url error:", e)
        return False


# =========================
# 🔹 WHATSAPP (BY NAME)
# =========================

def send_whatsapp_by_name(name, message):
    try:
        # Open WhatsApp Desktop
        subprocess.Popen("whatsapp:")
        time.sleep(6)  # load time

        # Search contact
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)

        pyautogui.write(name, interval=0.1)
        time.sleep(2)

        pyautogui.press("enter")
        time.sleep(1)

        # Type & send message
        pyautogui.write(message, interval=0.05)
        pyautogui.press("enter")

        return True

    except Exception as e:
        print("WhatsApp error:", e)
        return False


# =========================
# 🔹 EMAIL ACTION
# =========================

def send_email(to_email, subject, body):
    """
    Gmail App Password required
    """

    from_email = "YOUR_EMAIL@gmail.com"
    app_password = "YOUR_16_CHAR_APP_PASSWORD"

    msg = MIMEText(body)
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Email error:", e)
        return False


# =========================
# 🔹 MASTER EXECUTOR
# =========================

def execute_action(decision):
    action = decision.get("action")
    value = decision.get("value")

    if action == "OPEN_APP":
        return open_app(value)

    if action == "OPEN_URL":
        return open_url(value)

    if action == "SEND_WHATSAPP_NAME":
        return send_whatsapp_by_name(
            value["name"],
            value["message"]
        )

    if action == "SEND_EMAIL":
        return send_email(
            value["to"],
            value["subject"],
            value["body"]
        )

    return False

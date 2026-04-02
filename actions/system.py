import os
import time
import pyautogui

def volume_control(action_type):
    """Controls system volume."""
    try:
        if action_type == "UP":
            for _ in range(5):  # Increase by 10%
                pyautogui.press("volumeup")
            return "Volume increased."
        elif action_type == "DOWN":
            for _ in range(5):  # Decrease by 10%
                pyautogui.press("volumedown")
            return "Volume decreased."
        elif action_type == "MUTE":
            pyautogui.press("volumemute")
            return "System sound muted."
    except Exception as e:
        print("Volume Error:", e)
        return "Failed to change volume."

def media_control(action_type):
    """Controls system media playback."""
    try:
        if action_type == "PLAY_PAUSE":
            pyautogui.press("playpause")
            return "Media playback toggled."
        elif action_type == "NEXT":
            pyautogui.press("nexttrack")
            return "Skipping to next track."
        elif action_type == "PREV":
            pyautogui.press("prevtrack")
            return "Playing previous track."
    except Exception as e:
        print("Media Control Error:", e)
        return "Failed to control media."

def window_control(action_type):
    """Manages active windows."""
    try:
        if action_type == "MINIMIZE_ALL":
            pyautogui.hotkey('win', 'd')
            return "All windows minimized."
        elif action_type == "CLOSE_CURRENT":
            pyautogui.hotkey('alt', 'f4')
            return "Closed current window."
    except Exception as e:
        print("Window Control Error:", e)
        return "Failed to manage windows."

def take_screenshot():
    """Takes a screenshot and saves it to the desktop."""
    try:
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(desktop_dir, f"screenshot_{timestamp}.png")
        
        # Take the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return f"Screenshot saved to Desktop."
    except Exception as e:
        print("Screenshot Error:", e)
        return "Failed to take screenshot."

def system_power(action_type):
    """Executes system power states. Prompts confirmation prior to calling this."""
    try:
        if action_type == "SLEEP":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "System going to sleep."
        elif action_type == "RESTART":
            os.system("shutdown /r /t 5")
            return "Rebooting the computer."
        elif action_type == "SHUTDOWN":
            os.system("shutdown /s /t 5")
            return "Shutting down the computer."
    except Exception as e:
        print("Power Error:", e)
        return "Failed to execute power state."

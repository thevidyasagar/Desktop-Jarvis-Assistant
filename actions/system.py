import os
import time
import pyautogui
import subprocess

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
        elif action_type == "LOCK":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Laptop locked."
    except Exception as e:
        print("Power Error:", e)
        return "Failed to execute power state."

# --- NEW ADVANCED CONTROLS ---

def get_system_stats():
    """Returns a string description of CPU, RAM and Battery status."""
    try:
        cpu = subprocess.check_output('powershell "(Get-CimInstance Win32_Processor).LoadPercentage"', shell=True, text=True).strip()
        ram = subprocess.check_output('powershell "[int](((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize) * 100)"', shell=True, text=True).strip()
        battery = subprocess.check_output('powershell "(Get-CimInstance Win32_Battery).EstimatedChargeRemaining"', shell=True, text=True).strip()
        
        return f"Sir, your CPU load is at {cpu} percent, you have {ram} percent RAM free, and your battery is currently at {battery} percent charge."
    except Exception as e:
        return f"Failed to retrieve system stats: {e}"

def set_brightness(level):
    """Sets screen brightness (0-100)."""
    try:
        level = max(0, min(100, int(level)))
        cmd = f'powershell "Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods | Invoke-WmiMethod -MethodName WmiSetBrightness -ArgumentList 0,{level}"'
        subprocess.run(cmd, shell=True)
        return f"Screen brightness adjusted to {level} percent."
    except Exception as e:
        return f"Brightness adjustment failed: {e}"

def toggle_wifi(state):
    """Toggles WiFi admin state."""
    try:
        admin_state = "enabled" if state.lower() == "on" else "disabled"
        subprocess.run(f'powershell "netsh interface set interface Wi-Fi admin={admin_state}"', shell=True)
        return f"WiFi has been turned {state}."
    except Exception as e:
        return f"WiFi toggle failed: {e}"

def system_optimize():
    """Clears temporary files to optimize performance."""
    try:
        subprocess.run('powershell "Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"', shell=True)
        return "Optimization complete. Temporary files have been cleared."
    except Exception as e:
        return f"Optimization failed: {e}"

def get_active_window_title():
    """Detects the title of the currently focused window."""
    try:
        # Using PowerShell for robust native detection
        cmd = 'powershell "(Get-Process | Where-Object { $_.MainWindowHandle -eq (Get-ForegroundWindow) }).MainWindowTitle"'
        title = subprocess.check_output(cmd, shell=True, text=True).strip()
        return title if title else "Desktop"
    except Exception:
        return "Unknown"
    
def get_foreground_window():
    # Helper for PowerShell
    pass

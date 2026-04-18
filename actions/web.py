import os
import subprocess
import webbrowser
import urllib.parse
import time
import random
import pyautogui

def simulate_typing_search(base_url, query, focus_hotkey=None):
    """Helper to open a page, focus search, and type realistically."""
    webbrowser.open(base_url)
    time.sleep(3.0)  # Wait for page to realistically load
    
    if focus_hotkey:
        pyautogui.press(focus_hotkey)
        time.sleep(0.5)
        
    for char in query:
        pyautogui.write(char)
        time.sleep(random.uniform(0.03, 0.08))
        
    time.sleep(0.3)
    pyautogui.press('enter')

def google_search(query):
    """Searches Google for the given query realistically."""
    if not query:
        return "Please provide a subject to search."
    try:
        # Google homepage auto-focuses the search box
        simulate_typing_search("https://www.google.com", query)
        return f"Searching Google for {query}."
    except Exception as e:
        print("Google Search Error:", e)
        return "Failed to perform Google search."

def youtube_search(query):
    """Searches YouTube for the given query realistically."""
    if not query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    try:
        # YouTube uses '/' hotkey to focus search bar
        simulate_typing_search("https://www.youtube.com", query, focus_hotkey='/')
        return f"Searching YouTube for {query}."
    except Exception as e:
        print("YouTube Search Error:", e)
        return "Failed to perform YouTube search."

def wikipedia_search(query):
    """Searches Wikipedia realistically."""
    if not query:
        webbrowser.open("https://www.wikipedia.org")
        return "Opening Wikipedia."
    try:
        # We can just focus address bar and use wikipedia's search endpoint via omnibox,
        # or load Wikipedia and since it doesn't have a universal hotkey, just search google for "wikipedia {query}"
        # For simplicity and given prompt constraints, we'll try to use the omnibox search logic.
        webbrowser.open("about:blank")
        time.sleep(1.0)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        full_query = f"site:wikipedia.org {query}"
        for char in full_query:
            pyautogui.write(char)
            time.sleep(random.uniform(0.03, 0.08))
            
        pyautogui.press('enter')
        return f"Searching Wikipedia for {query}."
    except Exception as e:
        print("Wikipedia Search Error:", e)
        return "Failed to perform Wikipedia search."

def duckduckgo_search(query):
    if not query:
        webbrowser.open("https://duckduckgo.com")
        return "Opening DuckDuckGo."
    try:
        # DuckDuckGo auto-focuses on homepage
        simulate_typing_search("https://duckduckgo.com", query)
        return f"Searching DuckDuckGo for {query}."
    except Exception as e:
        print("DuckDuckGo Search Error:", e)
        return "Failed to perform DuckDuckGo search."

def amazon_search(query):
    if not query:
        webbrowser.open("https://www.amazon.com")
        return "Opening Amazon."
    try:
        # Amazon search bar doesn't consistently auto-focus or have a hotkey.
        # We'll use the browser's address bar to query amazon.
        webbrowser.open("about:blank")
        time.sleep(1.0)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        full_query = f"https://www.amazon.com/s?k="
        pyautogui.write(full_query, interval=0.01) # Write base URL fast
        # Then type query realistically
        for char in query:
            pyautogui.write(char)
            time.sleep(random.uniform(0.03, 0.08))
        pyautogui.press('enter')
        
        return f"Searching Amazon for {query}."
    except Exception as e:
        print("Amazon Search Error:", e)
        return "Failed to perform Amazon search."

def stackoverflow_search(query):
    if not query:
        webbrowser.open("https://stackoverflow.com")
        return "Opening Stack Overflow."
    try:
        webbrowser.open("about:blank")
        time.sleep(1.0)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        full_query = f"site:stackoverflow.com {query}"
        for char in full_query:
            pyautogui.write(char)
            time.sleep(random.uniform(0.03, 0.08))
        pyautogui.press('enter')
        return f"Searching Stack Overflow for {query}."
    except Exception as e:
        print("Stack Overflow Search Error:", e)
        return "Failed to perform Stack Overflow search."

def open_application(app_name):
    """Opens a local application or website."""
    if not app_name:
        return "Please provide an application name to open."
        
    app_name_lower = app_name.lower().strip()
    
    # Common local apps and websites
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "chrome": "start chrome",
        "edge": "start msedge",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "settings": "start ms-settings:",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "spotify": "start spotify",
        "vscode": "code .",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "whatsapp": "https://web.whatsapp.com",
        "github": "https://github.com",
        "chatgpt": "https://chat.openai.com",
    }
    
    try:
        if app_name_lower in apps:
            command_or_url = apps[app_name_lower]
            if command_or_url.startswith("http"):
                webbrowser.open(command_or_url)
                return f"Opening {app_name} website."
            else:
                if command_or_url.startswith("start "):
                    os.system(command_or_url)
                else:
                    subprocess.Popen(command_or_url, shell=True)
                return f"Opening local application {app_name}."
        else:
            # Fallback for websites if not in dictionary
            url = f"https://www.{app_name_lower.replace(' ', '')}.com"
            webbrowser.open(url)
            return f"Trying to open website for {app_name}."
    except Exception as e:
        print(f"Error opening application/website {app_name}:", e)
        return f"Failed to open {app_name}."

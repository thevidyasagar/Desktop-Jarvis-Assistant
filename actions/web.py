import os
import subprocess
import webbrowser
import urllib.parse

def google_search(query):
    """Searches Google for the given query."""
    if not query:
        return "Plese provide a subject to search."
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching Google for {query}."
    except Exception as e:
        print("Google Search Error:", e)
        return "Failed to perform Google search."

def youtube_search(query):
    """Searches YouTube for the given query."""
    if not query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    try:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching YouTube for {query}."
    except Exception as e:
        print("YouTube Search Error:", e)
        return "Failed to perform YouTube search."

def wikipedia_search(query):
    """Searches Wikipedia for the given query."""
    if not query:
        webbrowser.open("https://www.wikipedia.org")
        return "Opening Wikipedia."
    try:
        url = f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching Wikipedia for {query}."
    except Exception as e:
        print("Wikipedia Search Error:", e)
        return "Failed to perform Wikipedia search."

def duckduckgo_search(query):
    """Searches DuckDuckGo for the given query."""
    if not query:
        webbrowser.open("https://duckduckgo.com")
        return "Opening DuckDuckGo."
    try:
        url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching DuckDuckGo for {query}."
    except Exception as e:
        print("DuckDuckGo Search Error:", e)
        return "Failed to perform DuckDuckGo search."

def amazon_search(query):
    """Searches Amazon for the given query."""
    if not query:
        webbrowser.open("https://www.amazon.com")
        return "Opening Amazon."
    try:
        url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Searching Amazon for {query}."
    except Exception as e:
        print("Amazon Search Error:", e)
        return "Failed to perform Amazon search."

def stackoverflow_search(query):
    """Searches StackOverflow for the given query."""
    if not query:
        webbrowser.open("https://stackoverflow.com")
        return "Opening Stack Overflow."
    try:
        url = f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
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

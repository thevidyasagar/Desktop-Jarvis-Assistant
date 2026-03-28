import os
import json
import subprocess

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    r"C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
]

CACHE_FILE = "system/app_cache.json"


def scan_apps():
    apps = {}

    for base in START_MENU_PATHS:
        base = os.path.expandvars(base)
        for root, _, files in os.walk(base):
            for file in files:
                if file.endswith(".lnk"):
                    name = file.replace(".lnk", "").lower()
                    full_path = os.path.join(root, file)
                    apps[name] = full_path

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=2)

    return apps


def load_apps():
    if not os.path.exists(CACHE_FILE):
        return scan_apps()

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


APPS = load_apps()


def open_app(app_name):
    app_name = app_name.lower()

    for name, path in APPS.items():
        if app_name in name:
            subprocess.Popen(path, shell=True)
            return f"{name} opened."

    return None

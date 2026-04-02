import os
import json
import time
import pyautogui
from PIL import Image
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "screen_analysis.png")

def capture_screen():
    """Captures the current screen and returns the file path."""
    os.makedirs(os.path.dirname(SCREENSHOT_PATH), exist_ok=True)
    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_PATH)
    return SCREENSHOT_PATH

def analyze_screen(element_description, retries=2):
    """
    Uses Gemini Vision to find coordinates for a described UI element.
    Returns [ymin, xmin, ymax, xmax] in normalized 0-1000 coordinates.
    """
    path = capture_screen()
    
    prompt = f"""
    Find and locate the '{element_description}' in this screenshot.
    Return the result as a strict JSON object with the key 'box_2d' containing the coordinates in [ymin, xmin, ymax, xmax] format (normalized 0-1000) and a 'label' field.
    If multiple are found, return the most prominent one.
    If not found, return {{"box_2d": null, "label": "none"}}.
    """

    for attempt in range(retries + 1):
        try:
            # We use the new genai SDK which supports Gemini 2.0 Flash
            with open(path, "rb") as f:
                image_bytes = f.read()
                
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                ]
            )
            
            text = response.text.strip()
            # Clean markdown wrappers
            if text.startswith("```json"): text = text.split("```json")[1]
            elif text.startswith("```"): text = text.split("```")[1]
            if text.endswith("```"): text = text.rsplit("```", 1)[0]
            
            data = json.loads(text.strip())
            
            if data.get("box_2d"):
                print(f"🎯 Analysis Found {element_description}: {data['box_2d']}")
                return data["box_2d"]
                
            if attempt < retries:
                print(f"⚠️ Retrying detection ({attempt+1}/{retries})...")
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Screen Analysis Error (Attempt {attempt+1}): {e}")
            if attempt == retries: break
            time.sleep(1)

    return None

def get_pixel_coordinates(normalized_box):
    """
    Converts normalized 0-1000 coordinates to screen pixel coordinates.
    Returns (center_x, center_y).
    """
    if not normalized_box: return None
    
    ymin, xmin, ymax, xmax = normalized_box
    width, height = pyautogui.size()
    
    cx = ((xmin + xmax) / 2) / 1000 * width
    cy = ((ymin + ymax) / 2) / 1000 * height
    
    return int(cx), int(cy)

def show_visual_highlight(normalized_box):
    """
    Moves the mouse to trace a rectangle around the detected element to visually highlight it.
    """
    coords = get_pixel_coordinates(normalized_box)
    if not coords: return
    
    ymin, xmin, ymax, xmax = normalized_box
    width, height = pyautogui.size()
    
    # Calculate pixel bounds
    px_min = (xmin / 1000) * width
    py_min = (ymin / 1000) * height
    px_max = (xmax / 1000) * width
    py_max = (ymax / 1000) * height
    
    # Save current mouse pos
    original_pos = pyautogui.position()
    
    # Trace the highlight
    pyautogui.moveTo(px_min, py_min, duration=0.2)
    pyautogui.dragTo(px_max, py_min, duration=0.2)
    pyautogui.dragTo(px_max, py_max, duration=0.2)
    pyautogui.dragTo(px_min, py_max, duration=0.2)
    pyautogui.dragTo(px_min, py_min, duration=0.2)
    
    # Move back to center
    pyautogui.moveTo(coords[0], coords[1], duration=0.1)
    
    # Optional: return to original
    # pyautogui.moveTo(original_pos)

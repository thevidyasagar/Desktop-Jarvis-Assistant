import os
import re
import asyncio
import edge_tts
import time
import random
import pygame
import tempfile
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

# Local TTS Settings (edge-tts)
# Tuned for more natural, playful (natkhat) tone in Hindi/Hinglish
EDGE_VOICE = "en-IN-NeerjaNeural"
EDGE_RATE = "-2%"
EDGE_PITCH = "+1Hz"

# Track last filler to avoid immediate repetition
LAST_FILLER = None

def naturalize_text(text: str) -> str:
    """Enhances text with pauses and occasional playful Hinglish fillers."""
    global LAST_FILLER
    if not text:
        return text

    # Playful "natkhat" fillers (limited and varied)
    fillers = ["hmm...", "acha...", "ek second...", "ji sir...", "ji...", "waise...", "bilkul...", "toh..."]
    
    # 1. Replace major punctuation with '...' for natural pauses
    # But only if it's not already there
    natural_text = text
    if "..." not in text:
        natural_text = text.replace(", ", "... ").replace(". ", "... ").replace("! ", "... ").replace("? ", "...? ")
    
    # 2. Randomly insert a filler at the beginning (15% chance, down from 20%)
    # Skip if text already starts with a respectful prefix or acknowledgment
    skip_keywords = ["ji", "yes", "boliye", "theek hai", "hmm", "acha", "ok"]
    starts_with_ack = any(text.lower().startswith(kw) for kw in skip_keywords)

    if not starts_with_ack and random.random() < 0.15 and len(text.split()) > 3:
        # Choose a filler that isn't the same as the last one
        available_fillers = [f for f in fillers if f != LAST_FILLER]
        choice = random.choice(available_fillers)
        natural_text = f"{choice} {natural_text}"
        LAST_FILLER = choice
        
    # 3. Clean up any double pauses or trailing dots
    natural_text = natural_text.replace("....", "...").strip()
    
    # 4. Ensure it doesn't end abruptly if it's a short confirmation
    if len(text.split()) < 3 and not natural_text.endswith("...") and not natural_text.endswith("?"):
        natural_text = f"{natural_text} Sir"

    return natural_text

def clean_text_for_tts(text: str) -> str:
    """Cleans text for speech synthesis by removing emojis and special characters."""
    if not text:
        return text
        
    # 1. Remove emojis (non-ASCII characters)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # 2. Remove special symbols, keep normal punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,?!;:\"\'-]', ' ', text)
    
    # 3. Replace multiple dots (...) with a natural pause (comma)
    text = re.sub(r'\.{2,}', ',', text)
    
    # 4. Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def speak(text: str):
    """Centralized speak function using edge-tts with naturalization."""
    if not text:
        return
    
    # Apply naturalization (pauses/fillers)
    processed_text = naturalize_text(text)
    
    # Simple console output
    print(f"💬 SARA: {processed_text}")

    try:
        # Clean the text ONLY for speech
        speech_text = clean_text_for_tts(processed_text)
        
        # Run async edge-tts logic in the current thread
        asyncio.run(_speak_edge(speech_text))
    except Exception as e:
        print(f"❌ Speech failed: {e}")

async def _speak_edge(text: str):
    """Internal implementation using edge-tts and pygame playback."""
    try:
        communicate = edge_tts.Communicate(text=text, voice=EDGE_VOICE, rate=EDGE_RATE, pitch=EDGE_PITCH)
        temp_file = os.path.join(tempfile.gettempdir(), f"sara_voice_{int(time.time())}.mp3")
        await communicate.save(temp_file)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        
        # Cleanup temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass 
    except Exception as e:
        print(f"❌ edge-tts error: {e}")
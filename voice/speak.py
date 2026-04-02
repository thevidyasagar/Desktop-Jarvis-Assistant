import asyncio
import edge_tts
import tempfile
import os
import pygame
import time

VOICE = "en-IN-NeerjaNeural"
RATE = "+10%"
PITCH = "+2Hz"

def speak(text):
    if not text: return
    print(f"💬 SARA: {text}")

    async def _speak():
        communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE, pitch=PITCH)
        temp_file = os.path.join(tempfile.gettempdir(), f"sara_{int(time.time())}.mp3")
        await communicate.save(temp_file)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        try: os.remove(temp_file)
        except: pass

    asyncio.run(_speak())
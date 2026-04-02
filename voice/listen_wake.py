import sounddevice as sd
import numpy as np
import whisper
import webrtcvad
import noisereduce as nr

DEVICE = 9
RATE = 48000
SECONDS = 2
MIN_VOL = 0.01

# --- NEW CONFIG ---
VAD_MODE = 2
DEBUG_WAKE = True

vad = webrtcvad.Vad(VAD_MODE)
model = whisper.load_model("tiny.en")

def listen_wake():
    audio = sd.rec(
        int(SECONDS * RATE),
        samplerate=RATE,
        channels=1,
        device=DEVICE,
        dtype="float32",
        blocking=True
    )

    audio = np.squeeze(audio)

    # Basic volume check first (fastest)
    if np.max(np.abs(audio)) < MIN_VOL:
        return False
        
    # webrtcvad needs 10, 20, or 30ms frames.
    # RATE is 48000. 30ms is 48000 * 0.03 = 1440 samples
    chunk_size = int(RATE * 0.03)
    
    # Slice audio into 30ms chunks and check for speech
    has_speech = False
    for i in range(0, len(audio) - chunk_size, chunk_size):
        chunk = audio[i:i+chunk_size]
        pcm_data = (np.clip(chunk, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
        try:
            if vad.is_speech(pcm_data, RATE):
                has_speech = True
                break
        except Exception:
            pass
            
    if not has_speech:
        return False
        
    # If speech detected, reduce noise before transcribing
    try:
        audio = nr.reduce_noise(y=audio, sr=RATE, prop_decrease=0.8)
    except Exception as e:
        if DEBUG_WAKE: print("❌ Wake word noise reduction failed:", e)

    result = model.transcribe(
        audio,
        fp16=False,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result["text"].lower()
    if DEBUG_WAKE:
        print("👂 Wake raw:", text)

    return "sara" in text

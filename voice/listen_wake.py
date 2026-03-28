import sounddevice as sd
import numpy as np
import whisper

DEVICE = 9
RATE = 48000
SECONDS = 2
MIN_VOL = 0.01

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

    if np.max(np.abs(audio)) < MIN_VOL:
        return False

    result = model.transcribe(
        audio,
        fp16=False,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result["text"].lower()
    print("👂 Wake raw:", text)

    return "veda" in text

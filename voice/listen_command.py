import sounddevice as sd
import numpy as np
import whisper

DEVICE = 9
RATE = 48000
SECONDS = 4

model = whisper.load_model("tiny.en")

def listen_command():
    audio = sd.rec(
        int(SECONDS * RATE),
        samplerate=RATE,
        channels=1,
        device=DEVICE,
        dtype="float32",
        blocking=True
    )

    audio = np.squeeze(audio)

    result = model.transcribe(
        audio,
        fp16=False,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result["text"].strip().lower()
    print("🗣 Command:", text)

    return text

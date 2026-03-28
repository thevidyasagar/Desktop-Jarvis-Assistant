import sounddevice as sd
import numpy as np
import whisper

# ======================
# 🎙️ AUDIO CONFIG
# ======================
DEVICE_INDEX = 1  # 👈 Fixed device
SAMPLE_RATE = 16000
CHANNELS = 1
MIN_VOLUME = 0.001  # 👈 Lowered for better detection

sd.default.device = DEVICE_INDEX

print("🎤 Loading Whisper Base...")
model = whisper.load_model("base")
print("✅ Whisper ready")

def _record_dynamic(max_seconds=7):
    """Records until silence is detected or max_seconds reached"""
    print("🔴 Listening...")
    
    chunk_size = 1024
    recording = []
    silent_chunks = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        device=DEVICE_INDEX,   # 👈 FIXED
        channels=CHANNELS,
        dtype='float32'
    ) as stream:

        for _ in range(0, int(SAMPLE_RATE / chunk_size * max_seconds)):
            data, _ = stream.read(chunk_size)
            recording.append(data)

            volume = np.max(np.abs(data))
            # print("Volume:", volume)  # 👈 Debug (optional)

            if volume < MIN_VOLUME:
                silent_chunks += 1
            else:
                silent_chunks = 0

            # stop if silence ~1 sec
            if silent_chunks > (SAMPLE_RATE / chunk_size * 1):
                break

    if not recording:
        return np.array([])

    return np.concatenate(recording, axis=0).flatten()


def _transcribe(audio):
    if len(audio) < 1000:
        return "", None

    # normalize
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    result = model.transcribe(audio, fp16=False)
    text = result.get("text", "").strip().lower()

    print("📝 You said:", text)  # 👈 Debug output

    return text, result.get("language")


def listen():
    try:
        audio = _record_dynamic(max_seconds=4)
        return _transcribe(audio)
    except Exception as e:
        print("❌ Error:", e)
        return "", None


def listen_command():
    return listen()
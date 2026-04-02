import sounddevice as sd
import numpy as np
import whisper
import webrtcvad
import noisereduce as nr
import time

# ======================
# 🎙️ AUDIO CONFIG
# ======================
DEVICE_INDEX = None  # 👈 Use system default microphone
SAMPLE_RATE = 16000
CHANNELS = 1
MIN_VOLUME = 0.005  # RMS Fallback threshold

# --- NEW CONFIG ---
VAD_MODE = 2  # 0: Normal, 1: Low Bitrate, 2: Aggressive, 3: Very Aggressive
DEBUG_AUDIO = True  # Set to True to see [V] vs [-] for debugging

vad = webrtcvad.Vad(VAD_MODE)

print("🎤 Loading Whisper Base...")
model = whisper.load_model("base")
print("✅ Whisper ready")


def calibrate_mic(seconds=1.5):
    """Automatically adjusts microphone sensitivity to room background noise."""
    global MIN_VOLUME
    print("🎙️ Adjusting to background noise... please wait 1 second.")
    chunk_size = 1024
    recording = []
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, device=DEVICE_INDEX, channels=CHANNELS, dtype='float32') as stream:
            for _ in range(0, int(SAMPLE_RATE / chunk_size * seconds)):
                data, _ = stream.read(chunk_size)
                rms = np.sqrt(np.mean(data**2))  # RMS energy calculation
                recording.append(rms)
        avg_noise = np.mean(recording)
        # Set threshold dynamically: well above background noise, with a strict minimum
        MIN_VOLUME = max(avg_noise * 3.5, 0.001)
        if DEBUG_AUDIO:
            print(f"✅ Microphone calibrated! Baseline noise: {avg_noise:.5f}, Threshold: {MIN_VOLUME:.5f}")
        else:
            print("✅ Microphone calibrated for your room!")
    except Exception as e:
        print("❌ Calibration failed, using default threshold.", e)

# Calibrate automatically as soon as the assistant boots
calibrate_mic()

def _record_dynamic(max_seconds=10, idle_timeout=60):
    """Waits for voice, then records until silence is detected. Returns TIMEOUT if completely silent."""
    print("🔴 Sara is Listening...")
    
    # WebRTCVAD accepts 10, 20, or 30 ms frames. We use 30 ms.
    chunk_length_ms = 30
    chunk_size = int(SAMPLE_RATE * chunk_length_ms / 1000)  # 480 samples at 16000 Hz
    
    recording = []
    pre_buffer = []  # Keep a short buffer of audio before voice triggers
    
    has_spoken = False
    silent_chunks = 0
    speech_chunks = 0
    start_time = time.time()
    
    # Buffer up to 1 second of audio (approx 33 chunks)
    max_pre_buffer = int(1000 / chunk_length_ms)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        device=DEVICE_INDEX,
        channels=CHANNELS,
        blocksize=chunk_size,
        dtype='float32'
    ) as stream:

        while True:
            # We must be careful to only read exactly chunk_size length arrays for VAD
            data, _ = stream.read(chunk_size)
            volume = np.sqrt(np.mean(data**2))
            
            # Convert float32 to int16 PCM for WebRTCVAD
            pcm_data = (np.clip(data, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
            
            try:
                is_speech = vad.is_speech(pcm_data, SAMPLE_RATE)
            except Exception as e:
                is_speech = False
                
            # Both VAD and Volume threshold are required to avoid false positives on sudden sharp noises
            is_valid_speech = is_speech and (volume > MIN_VOLUME)
            
            if DEBUG_AUDIO:
                print("V" if is_speech else "-", end="", flush=True)

            if not has_spoken:
                # If silent for too long, exit with TIMEOUT
                if (time.time() - start_time) > idle_timeout:
                    if DEBUG_AUDIO: print()
                    return "TIMEOUT"

                # Still waiting for speech to begin
                pre_buffer.append(data.copy())
                if len(pre_buffer) > max_pre_buffer:
                    pre_buffer.pop(0)  # Keep only the most recent chunks
                    
                if is_valid_speech:
                    has_spoken = True
                    if DEBUG_AUDIO: print("\n🗣️ Sound detected, recording...")
                    else: print("🗣️ Sound detected, recording...")
                    recording.extend(pre_buffer)
                    silent_chunks = 0
            else:
                # We are actively recording a sentence
                recording.append(data.copy())
                speech_chunks += 1
                
                if not is_valid_speech:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                
                # Stop if silence ~1.5 sec (1500 ms / 30 ms = 50 chunks)
                if silent_chunks > (1500 / chunk_length_ms):
                    if DEBUG_AUDIO: print("\n✅ Finished speaking.")
                    break
                    
                # Hard limit to 15 seconds (15000 ms / 30 ms = 500 chunks)
                if speech_chunks > (15000 / chunk_length_ms):
                    if DEBUG_AUDIO: print("\n🛑 Reached 15s time limit.")
                    break

    if DEBUG_AUDIO: print()
    
    if not recording:
        return np.array([])
        
    audio_array = np.concatenate(recording, axis=0).flatten()
    
    # --- NOISE REDUCTION ---
    if DEBUG_AUDIO: print("🧹 Applying noise reduction...")
    try:
        reduced_audio = nr.reduce_noise(y=audio_array, sr=SAMPLE_RATE, prop_decrease=0.8)
        return reduced_audio
    except Exception as e:
        print("❌ Noise reduction failed:", e)
        return audio_array


def _transcribe(audio):
    # Require at least 0.5 seconds of audio to transcribe (16000 * 0.5 = 8000 samples)
    if len(audio) < 8000:
        return "", None

    # condition_on_previous_text=False stops Whisper from hallucinating/repeating itself on weird noises
    result = model.transcribe(audio, fp16=False, condition_on_previous_text=False)
    text = result.get("text", "").strip().lower()

    if DEBUG_AUDIO:
        print("📝 Transcription raw output:", text)

    return text, result.get("language")


def listen(idle_timeout=60):
    try:
        audio_or_timeout = _record_dynamic(max_seconds=10, idle_timeout=idle_timeout)
        if isinstance(audio_or_timeout, str) and audio_or_timeout == "TIMEOUT":
            return "TIMEOUT", None
        return _transcribe(audio_or_timeout)
    except Exception as e:
        print("❌ Error:", e)
        return "", None


def listen_command():
    return listen()
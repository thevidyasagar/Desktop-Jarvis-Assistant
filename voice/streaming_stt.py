import os
import queue
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from voice.hardware import get_optimal_whisper_specs
from voice.audio_engine import AudioEngine

# Config
SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 30 # For VAD
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)

class StreamingSTT:
    def __init__(self):
        self.model_size, self.compute_type = get_optimal_whisper_specs()
        print(f"🎙️ Initializing Faster-Whisper ({self.model_size})...")
        self.model = WhisperModel(self.model_size, device="cuda" if "large" in self.model_size or "medium" in self.model_size else "cpu", compute_type=self.compute_type)
        
        self.audio_engine = AudioEngine()
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        self.recording_buffer = []
        self.is_recording = False
        self.silence_chunks = 0
        
    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"⚠️ Audio Status: {status}")
        self.audio_queue.put(indata.copy().flatten())

    def start(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=CHUNK_SIZE, 
                            dtype='float32', callback=self._audio_callback):
            while self.is_listening:
                try:
                    chunk = self.audio_queue.get(timeout=1)
                    res = self.audio_engine.process_chunk(chunk)
                    
                    if res["is_speech"]:
                        if not self.is_recording:
                            print("\n🗣️ Speech detected...")
                            self.is_recording = True
                        self.recording_buffer.append(chunk)
                        self.silence_chunks = 0
                    elif self.is_recording:
                        self.recording_buffer.append(chunk)
                        self.silence_chunks += 1
                        
                        # Stop after ~1 second of silence
                        if self.silence_chunks > (1000 / CHUNK_DURATION_MS):
                            self.is_recording = False
                            audio_data = np.concatenate(self.recording_buffer)
                            self.recording_buffer = []
                            self._transcribe(audio_data)
                except queue.Empty:
                    continue

    def _transcribe(self, audio_data):
        segments, info = self.model.transcribe(audio_data, beam_size=5, initial_prompt="SARA, Mera chrome kholo. Stop. Ruk jao.")
        text = " ".join([seg.text for seg in segments]).strip().lower()
        if text:
            print(f"📝 Transcribed: {text} ({info.language})")
            
            # Check for immediate interruptions
            if any(p in text for p in ["stop", "ruk jao", "bas karo", "quiet"]):
                from voice.speak import stop_speaking
                stop_speaking()
                
            self.last_transcription = text
            self.last_lang = info.language

    def listen(self):
        """Blocking call to get the next transcription."""
        self.last_transcription = None
        self.start()
        while self.is_listening:
            if hasattr(self, 'last_transcription') and self.last_transcription:
                text = self.last_transcription
                lang = self.last_lang
                self.last_transcription = None
                self.is_listening = False # Stop for now to process
                return text, lang
            time.sleep(0.1)

# Singleton instance
stt_engine = StreamingSTT()

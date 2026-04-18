from voice.speak import speak
import os

# Test 1: Fallback (without API key)
print("--- Testing Fallback (No context for ElevenLabs) ---")
os.environ["ELEVENLABS_API_KEY"] = ""  # Temporarily clear to force fallback
speak("Hello Sir... Testing the local fallback system.")

# Test 2: Caching Logic
print("\n--- Testing Caching Logic ---")
text = "I am SARA, your personal AI assistant... ready to help."
speak(text)  # First time (should be slow/fallback)
speak(text)  # Second time (should be from cache)

print("\nVerification script finished. Please check the audio output.")

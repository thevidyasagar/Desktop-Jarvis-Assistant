import os
from unittest.mock import MagicMock, patch
import importlib
import voice.speak

def test_api_detection():
    print("\n--- Testing API Detection Logic ---")
    
    # Case 1: Modern SDK (v1.0+)
    print("\n[Test 1] Simulating Modern SDK (v1.0+)")
    mock_client_v1 = MagicMock()
    # Ensure hasattr(mock_client_v1, "text_to_speech") is True
    # And hasattr(mock_client_v1.text_to_speech, "convert") is True
    mock_client_v1.text_to_speech.convert = MagicMock(return_value=[b"audio_chunk"])
    
    with patch("voice.speak.client", mock_client_v1):
        voice.speak.speak("Modern SDK test")
        if mock_client_v1.text_to_speech.convert.called:
            print("✅ Successfully detected and called Modern SDK convert()")
        else:
            print("❌ Failed to detect Modern SDK")

    # Case 2: Legacy SDK
    print("\n[Test 2] Simulating Legacy SDK")
    mock_client_legacy = MagicMock(spec=["generate"]) # Only has generate
    mock_client_legacy.generate.return_value = [b"legacy_chunk"]
    
    # We need to make sure hasattr(mock_client_legacy, "text_to_speech") is False
    # MagicMock usually returns another mock for any attribute, so we use spec.
    
    with patch("voice.speak.client", mock_client_legacy):
        voice.speak.speak("Legacy SDK test")
        if mock_client_legacy.generate.called:
            print("✅ Successfully detected and called Legacy SDK generate()")
        else:
            print("❌ Failed to detect Legacy SDK")

if __name__ == "__main__":
    test_api_detection()

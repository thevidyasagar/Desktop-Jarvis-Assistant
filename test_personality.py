from core.brain import ask_jarvis
import os
import sys

# Ensure API key is available (it's expected to be in the environment)
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

def test_personality():
    """
    Test SARA's personality by asking about its creator and boss.
    """
    queries = [
        "Who is your creator?",
        "Who is your boss?",
        "Who made you?",
        "Who is the admin?",
        "Who is the master mind behind SARA?"
    ]
    
    print("=" * 40)
    print("S.A.R.A. Personality Verification")
    print("=" * 40)
    
    for query in queries:
        print(f"\n[User]: {query}")
        try:
            # History is empty for independent tests
            reply, _ = ask_jarvis(query)
            print(f"[SARA]: {reply}")
        except Exception as e:
            print(f"[ERROR]: Failed to get response from brain. {e}")
        print("-" * 40)

if __name__ == "__main__":
    test_personality()

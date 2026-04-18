import sys
import os
import json

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.proactive import get_proactive_suggestion

def test_proactive():
    # Simulate empty history (idle state)
    print("--- Testing Idle State (Empty History) ---")
    idle_context = """
--- STRUCTURED MEMORY LEVEL ---
LAST OPENED APP: None
LAST EXECUTED COMMAND: None
FAVORITE COMMANDS: None yet

--- SHORT TERM HISTORY (Oldest to Newest) ---
No recent history.
"""
    result = get_proactive_suggestion(idle_context)
    if result:
        print(f"Suggestion: {result['text']}")
    else:
        print("No suggestion made.")

    print("\n--- Testing Active State ---")
    active_context = """
--- STRUCTURED MEMORY LEVEL ---
LAST OPENED APP: chrome
LAST EXECUTED COMMAND: OPEN_APP
FAVORITE COMMANDS: OPEN_APP (5x), SEARCH_FILE (2x)

--- SHORT TERM HISTORY (Oldest to Newest) ---
- Action: OPEN_APP | Target: chrome | Result: Completed
- AI Replied Conversational: I have opened Chrome for you.
"""
    result = get_proactive_suggestion(active_context)
    if result:
        print(f"Suggestion: {result['text']}")
    else:
        print("No suggestion made.")

if __name__ == "__main__":
    test_proactive()

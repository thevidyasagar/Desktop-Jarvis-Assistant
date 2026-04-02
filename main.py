import re
import time
import threading
from voice.listen import listen
from voice.speak import speak
from core.brain import ask_jarvis
from core.planner import generate_plan
from core.action import execute_action
from core.memory import MemoryManager
from core.vision import start_vision, stop_vision
from core.screen import analyze_screen, get_pixel_coordinates, show_visual_highlight
from actions.files import smart_search
from core.proactive import get_proactive_suggestion
from actions.system import volume_control, media_control, window_control, take_screenshot, system_power, get_active_window_title

WAKE_PATTERNS = ["sara", "sar", "sa", "sra", "saara", "tara", "zara", "zarah"]

CONFIRMATION_WORDS = ["yes", "go ahead", "do it", "sure", "karo", "haan", "theek hai", "ok", "okay", "please", "confirm"]

def is_wake_word(text: str) -> bool:
    text = re.sub(r"[^\w\s]", "", text.lower()).strip()
    return any(p.lower() in text for p in WAKE_PATTERNS)

def is_confirmation(text: str) -> bool:
    text = re.sub(r"[^\w\s]", "", text.lower()).strip()
    # Simple check for confirmation keywords in the user's short response
    return any(word in text.split() for word in CONFIRMATION_WORDS)

def schedule_thread(delay, message):
    time.sleep(delay)
    print(f"\n⏰ Reminder: {message}")
    speak(f"Sir, I have a reminder for you: {message}")

def start_veda():
    print("🟢 Sara Online")
    speak("Hello Sir, this is Sara. I’m ready to assist you?")
    
    conversation = []
    memory = MemoryManager()

    while True:
        text, _ = listen()
        if text == "TIMEOUT":
            # The user has been quiet for 60 seconds
            if memory.can_suggest(cooldown_seconds=1800): # 30 min cooldown
                print("🧠 Checking for helpful suggestions...")
                suggestion_data = get_proactive_suggestion(memory.get_context_string())
                if suggestion_data:
                    speak(suggestion_data["text"])
                    memory.add_proactive_history(suggestion_data["text"])
                    if suggestion_data.get("action"):
                        memory.set_pending_action(suggestion_data["action"])
            continue
            
        if not text: continue

        if is_wake_word(text):
            speak("Yes Sir?") # Quick response
            
            command, lang = listen() # Listen for actual command
            if not command: continue
            
            user_text = command.lower()
            print(f"🎯 Command: {user_text}")

            # --- AUTONOMOUS MODE CHECK ---
            pending = memory.get_pending_action()
            plan = None
            
            if pending:
                # 60 second expiry check
                if (time.time() - memory.get_pending_action_time()) < 60:
                    if is_confirmation(user_text):
                        print("🤖 Autonomous Action Confirmed!")
                        plan = pending
                        memory.clear_pending_action()
                    else:
                        print("🗑️ Different command received, clearing pending action.")
                        memory.clear_pending_action()
                else:
                    print("⏰ Pending action expired.")
                    memory.clear_pending_action()

            # Planner & Task Execution (Fallback if no pending action was confirmed)
            if not plan:
                print("🧠 Planning Tasks...")
                plan = generate_plan(user_text, memory.get_context_string())
            
            # Direct Conversation Route
            if len(plan) == 1 and plan[0].get("action") == "CONVERSATION":
                reply, conversation = ask_jarvis(user_text, conversation, lang)
                speak(reply)
                memory.add_conversation(reply)
                continue
                
            # Execute Sequential Plan
            if len(plan) > 1:
                speak(f"Executing {len(plan)} tasks sequentially.")
                
            for step in plan:
                action = step.get("action")
                value = step.get("value")
                
                if not action or action == "NONE":
                    continue
                
                # --- NEW INTERNAL AI EXECUTORS ---
                if action == "EXIT_PROGRAM":
                    speak("Goodbye Sir. System offline.")
                    return  # Break completely out of the program loop
                    
                if action == "CLEAR_MEMORY":
                    result = memory.clear_memory()
                    speak(result)
                    continue
                    
                if action == "ENABLE_VISION":
                    result = start_vision(memory)
                    speak(result)
                    memory.add_history("ENABLE_VISION", None, "Camera Enabled")
                    continue
                    
                if action == "DISABLE_VISION":
                    result = stop_vision()
                    speak(result)
                    memory.add_history("DISABLE_VISION", None, "Camera Disabled")
                    continue
                    
                if action == "SEARCH_FILE":
                    speak(f"Searching for {value}...")
                    results = smart_search(value)
                    if results:
                        top = results[0]
                        speak(f"I found a match: {top['name']}. Should I open it?")
                        # Save the actual open action as a pending action
                        memory.set_pending_action([{"action": "OPEN_FILE", "value": top["path"]}])
                        continue
                    else:
                        speak(f"Sir, I couldn't find any file matching {value}. Would you like to try a different name?")
                        continue

                if action == "VISUAL_CLICK":
                    speak(f"Analyzing the screen for the {value}...")
                    box = analyze_screen(value)
                    if box:
                        coords = get_pixel_coordinates(box)
                        show_visual_highlight(box)
                        speak(f"I found it! Should I proceed to click the {value} highlighted on your screen?")
                        # Save the actual click action as a pending action for the user to confirm
                        memory.set_pending_action([{"action": "CLICK_AT", "value": {"x": coords[0], "y": coords[1]}}])
                        continue
                    else:
                        speak(f"Sir, I couldn't clearly locate the {value}. Would you like me to try another scan?")
                        continue

                if action == "UPDATE_USER_PROFILE":
                    speak(memory.update_user_profile(value.get("key"), value.get("value")))
                    continue

                if action == "DELETE_USER_PROFILE":
                    speak(memory.delete_user_profile_item(value))
                    continue

                if action == "SCHEDULE_REMINDER":
                    if isinstance(value, dict):
                        delay = value.get("delay_seconds", 0)
                        msg = value.get("message", "Reminder")
                        target_time = time.time() + delay
                        speak(memory.add_reminder(target_time, msg))
                    continue
                
                # Execute standard task via action.py
                print(f"⚙️ Executing step: {action} ({value})")
                execution_result = execute_action(step)
                
                result_str = execution_result if execution_result else "Completed without message"
                if execution_result:
                    speak(execution_result)
                    
                memory.add_history(action, value, result_str)

if __name__ == "__main__":
    start_veda()
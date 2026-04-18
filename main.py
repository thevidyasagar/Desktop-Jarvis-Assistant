import sys
import re
import time
import random
from voice.speak import speak
from core.brain import ask_jarvis
from core.planner import generate_plan
from core.action import execute_action
from core.memory import MemoryManager
from core.vision import start_vision, stop_vision
from core.screen import analyze_screen, get_pixel_coordinates, show_visual_highlight
from actions.files import smart_search
from voice.listen import listen_command
from core.proactive import check_proactive as core_check_proactive, update_interaction_time
# from core.presence import start_presence, stop_presence

WAKE_PATTERNS = ["sara", "sar", "sa", "sra", "saara", "tara", "zara", "zarah", "tarah", "lara"]
CONFIRMATION_WORDS = ["yes", "go ahead", "do it", "sure", "karo", "haan", "theek hai", "ok", "okay", "please", "confirm"]

def detect_and_strip_wake_word(text: str) -> tuple[bool, str]:
    """Detects if a wake word is used as a prefix and returns (has_wake, cleaned_text)."""
    text_lower = text.lower().strip()
    # Normalize for comparison: remove punctuation
    clean_text = re.sub(r"[^\w\s]", "", text_lower).strip()
    
    if not clean_text:
        return False, ""

    # Sort patterns by length descending to match longest first
    sorted_patterns = sorted(WAKE_PATTERNS, key=len, reverse=True)
    
    for p in sorted_patterns:
        # Match pattern at the start of the string with a word boundary
        pattern_regex = rf"^{p}\b"
        if re.search(pattern_regex, clean_text):
            # Remaining content after stripping wake word
            remaining = re.sub(pattern_regex, "", clean_text).strip()
            return True, remaining
            
    return False, clean_text

def is_confirmation(text: str) -> bool:
    text = re.sub(r"[^\w\s]", "", text.lower()).strip()
    return any(word in text.split() for word in CONFIRMATION_WORDS)

class AssistantCore:
    def __init__(self):
        self.memory = MemoryManager()
        self.conversation = []
        self.last_response = ""

    def get_greeting(self):
        greetings = [
                 "Hi Sir... aa gaye aap finally... mujhe laga bhool hi gaye hai aap😊🤣...",
                 "Namaste Sir... main to kabse wait kar rahi thi aapka😁... ab bataiye kya karna hai?",
                 "Hello Sir... sab theek hai na😒...? ya phir sirf mujhe yaad kar rahe the",
                 "Acha... toh aap aa hi gaye... aaj kya special plan hai mere saath?",
                 "Ji Boss... mai to ready hi thi... bas aapka hi intezaar kar rhi thi...",
                 "Swagat hai Sir... Sara reporting for duty... aur thodi si aapki bhi hu",
                 "Hmm boss... aaj kaafi late aaye ho boss... busy the ya mujhe miss kar rahe the?",
                 "Finally aap aa gaye boss... ab bataiye... kaam karna hai ya sirf baatein hi karni hain?"
        ]
        greet = random.choice(greetings)
        self.last_response = greet
        return greet

    def process_text(self, user_text: str, lang: str = "en") -> str:
        """Processes user input and returns the Assistant's verbal response."""
        print(f"🎯 Processing: {user_text}")
        
        has_wake, cleaned_text = detect_and_strip_wake_word(user_text)
        
        # Determine what text to actually process
        processing_text = cleaned_text if has_wake else user_text
        
        prefix = ""
        if has_wake:
            if not cleaned_text:
                # Case 1: Only wake word
                acknowledgments = ["Yes Sir?", "Ji Sir?", "Boliye Sir?", "Hmm, sun rahi hoon...", "Ji, kahiye?"]
                reply = random.choice(acknowledgments)
                self.last_response = reply
                return reply
            else:
                # Case 2: Wake word + command
                prefixes = ["Ji Sir...", "Yes Sir...", "Boliye Sir...", "Ji boss...", "Ji Bilkul...", "Theek hai Sir..."]
                prefix = random.choice(prefixes) + " "
        
        # Case 3: Process normally (with or without prefix setup above)
        
        # --- AUTONOMOUS MODE CHECK ---
        pending = self.memory.get_pending_action()
        plan = None
        
        if pending:
            # 60 second expiry check
            if (time.time() - self.memory.get_pending_action_time()) < 60:
                if is_confirmation(processing_text):
                    print("🤖 Autonomous Action Confirmed!")
                    plan = pending
                    self.memory.clear_pending_action()
                else:
                    print("🗑️ Different command received, clearing pending action.")
                    self.memory.clear_pending_action()
            else:
                print("⏰ Pending action expired.")
                self.memory.clear_pending_action()
        
        # Planner & Task Execution (Fallback if no pending action was confirmed)
        if not plan:
            print("🧠 Planning Tasks...")
            plan = generate_plan(processing_text, self.memory.get_context_string())
        
        # Direct Conversation Route
        if len(plan) == 1 and plan[0].get("action") == "CONVERSATION":
            reply, self.conversation = ask_jarvis(processing_text, self.conversation, lang)
            self.memory.add_conversation(reply)
            # Combine prefix with conversation reply
            final_reply = prefix + reply
            self.last_response = final_reply
            return final_reply
            
        # Execute Sequential Plan
        response_msg = ""
        if len(plan) > 1:
            response_msg = f"Executing {len(plan)} tasks sequentially. "
            
        for step in plan:
            action = step.get("action")
            value = step.get("value")
            
            if not action or action == "NONE":
                continue
            
            # --- INTERNAL AI EXECUTORS ---
            if action == "EXIT_PROGRAM":
                return "EXIT_SIGNAL"
                
            if action == "CLEAR_MEMORY":
                result = self.memory.clear_memory()
                response_msg += result
                continue
                
            if action == "ENABLE_VISION":
                result = start_vision(self.memory)
                response_msg += result
                self.memory.add_history("ENABLE_VISION", None, "Camera Enabled")
                continue
                
            if action == "DISABLE_VISION":
                result = stop_vision()
                response_msg += result
                self.memory.add_history("DISABLE_VISION", None, "Camera Disabled")
                continue
                
            if action == "SEARCH_FILE":
                results = smart_search(value)
                if results:
                    top = results[0]
                    msg = f"I found a match: {top['name']}. Should I open it?"
                    self.memory.set_pending_action([{"action": "OPEN_FILE", "value": top["path"]}])
                    response_msg += msg
                else:
                    response_msg += f"Sir, I couldn't find any file matching {value}."
                continue

            if action == "VISUAL_CLICK":
                box = analyze_screen(value)
                if box:
                    coords = get_pixel_coordinates(box)
                    show_visual_highlight(box)
                    msg = f"I found it! Should I proceed to click the {value}?"
                    self.memory.set_pending_action([{"action": "CLICK_AT", "value": {"x": coords[0], "y": coords[1]}}])
                    response_msg += msg
                else:
                    response_msg += f"Sir, I couldn't clearly locate the {value}."
                continue

            if action == "UPDATE_USER_PROFILE":
                response_msg += self.memory.update_user_profile(value.get("key"), value.get("value"))
                continue

            if action == "DELETE_USER_PROFILE":
                response_msg += self.memory.delete_user_profile_item(value)
                continue

            if action == "SCHEDULE_REMINDER":
                if isinstance(value, dict):
                    delay = value.get("delay_seconds", 0)
                    msg = value.get("message", "Reminder")
                    target_time = time.time() + delay
                    response_msg += self.memory.add_reminder(target_time, msg)
                continue
            
            # Execute standard task via action.py
            print(f"⚙️ Executing step: {action} ({value})")
            execution_result = execute_action(step)
            
            result_str = execution_result if execution_result else "Completed"
            if execution_result:
                response_msg += execution_result + " "
                
            self.memory.add_history(action, value, result_str)

        self.last_response = (prefix + response_msg.strip()).strip()
        return self.last_response

    def check_proactive(self):
        """Checks for proactive suggestions."""
        suggestion = core_check_proactive()
        if suggestion:
            self.memory.add_proactive_history(suggestion)
            return suggestion
        return None

if __name__ == "__main__":
    print("🚀 Assistant started...........")
    assistant = AssistantCore()
    
    # Start Background Presence Monitoring (Temporarily Disabled)
    # start_presence()
    
    # 1. Greet User
    greeting = assistant.get_greeting()
    speak(greeting)
    print(f"SARA: {greeting}")
    
    print("🔵 SYSTEM ONLINE BOSS.....")
    
    try:
        while True:
            # 2. Check for Proactive Suggestions
            proactive_result = assistant.check_proactive()
            if proactive_result:
                suggestion_text, pending_action = proactive_result
                speak(suggestion_text)
                print(f"SARA (Proactive): {suggestion_text}")
                if pending_action:
                    assistant.memory.set_pending_action([pending_action])

            # 3. Listen for Command
            print("🎤 Listening...")
            text, lang = listen_command()
            
            if text and text != "TIMEOUT":
                update_interaction_time()
                print(f"YOU: {text}")
                
                # 4. Process Input
                response = assistant.process_text(text, lang)
                
                if response == "EXIT_SIGNAL":
                    exit_msg = "Theek hai Sir, switching off. Alvida!"
                    speak(exit_msg)
                    print(f"VEDA: {exit_msg}")
                    # stop_presence()
                    sys.exit(0)
                    
                # 5. Speak and Print Response
                if response:
                    speak(response)
                    print(f"SARA: {response}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 System Shutting Down...")
        # stop_presence()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Critical Error in Main Loop: {e}")
        import traceback
        traceback.print_exc()
        # stop_presence()
        sys.exit(1)

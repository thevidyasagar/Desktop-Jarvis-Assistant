import time
import random
import threading

try:
    from core.brain import generate_proactive_suggestion_ai
except ImportError:
    generate_proactive_suggestion_ai = None

last_interaction_time = time.time()
last_proactive_fire_time = 0.0

COOLDOWN_LIMIT = 150  # 150 seconds (2.5 mins) between suggestions

IDLE_SUGGESTIONS = [
    (
        "Sir... kaafi chup hai aaj aap 😏... bore ho rahe hai kya... YouTube pe kuch Intresting sa laga du?",
        {"action": "OPEN_URL", "value": "https://www.youtube.com"}
    ),
    (
        "Itne serious mat raha kariye boss 😄... aap relax raha kariye mai hu na... kuch dekhna hai kya aapko?",
        {"action": "OPEN_APP", "value": "chrome"}
    ),
    (
        "Boss... aap chup kyu hai inti der se 😏... mujhe ignore kar rahe ho kya?",
        None
    ),
    (
        "Aree Sir... Kuch kaam karna hai ya bas mujhe hi dekhte rahoge 😄... bolo kya open karu aapke liye?",
        None
    ),
    (
        "Hmm boss... main yaha aise bore ho rahi hu 😏... koi kaam hai mere liye ya bas aise hi wait karti rhu?",
        None
    )
]

ai_suggestions_cache = []
ai_generation_in_progress = False
last_suggestion_text = ""
last_ai_attempt_time = 0.0

def _generate_and_cache_ai():
    global ai_generation_in_progress, ai_suggestions_cache, last_ai_attempt_time
    ai_generation_in_progress = True
    try:
        if generate_proactive_suggestion_ai:
            text = generate_proactive_suggestion_ai()
            if text:
                ai_suggestions_cache.append((text, None))
            else:
                # If generation returns None (e.g., failed safely), trigger backoff
                last_ai_attempt_time = time.time()
    except Exception as e:
        print("Async AI pre-gen failed:", e)
        # Trigger backoff on exception
        last_ai_attempt_time = time.time()
    finally:
        ai_generation_in_progress = False

def trigger_ai_cache_refill():
    global ai_generation_in_progress, ai_suggestions_cache, last_ai_attempt_time
    
    # Enforce a 60-second backoff if the last API call failed/was exhausted
    if time.time() - last_ai_attempt_time < 60:
        return
        
    if not ai_generation_in_progress and len(ai_suggestions_cache) < 2:
        th = threading.Thread(target=_generate_and_cache_ai, daemon=True)
        th.start()

def update_interaction_time():
    """Update the timestamp of the user's last command or speech."""
    global last_interaction_time
    last_interaction_time = time.time()

def check_proactive():
    """Checks for proactive suggestions based on pure interaction time."""
    global last_interaction_time, last_proactive_fire_time, last_suggestion_text, ai_suggestions_cache
    
    current_time = time.time()
    
    # Try to keep memory cache filled slowly in background
    trigger_ai_cache_refill()
    
    # If user hasn't interacted for 120 seconds
    if current_time - last_interaction_time > 120:
        # Check if enough time has passed since our last suggestion (Cooldown)
        if current_time - last_proactive_fire_time > COOLDOWN_LIMIT:
            
            # 70% AI, 30% Predefined
            use_ai = random.random() < 0.70
            suggestion_tuple = None
            
            if use_ai and len(ai_suggestions_cache) > 0:
                suggestion_tuple = ai_suggestions_cache.pop(0)
                # Spin background job proactively
                trigger_ai_cache_refill()
            else:
                # Fallback to predefined safely avoiding instant repetition
                valid_predefined = [s for s in IDLE_SUGGESTIONS if s[0] != last_suggestion_text]
                if not valid_predefined:
                    valid_predefined = IDLE_SUGGESTIONS
                suggestion_tuple = random.choice(valid_predefined)
                
            last_proactive_fire_time = current_time
            last_suggestion_text = suggestion_tuple[0]
            
            print(f"💡 [PROACTIVE] TIME_IDLE logic fired: {suggestion_tuple[0]}")
            return suggestion_tuple
            
    return None

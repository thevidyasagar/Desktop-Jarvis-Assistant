import os
import json
import time
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "memory.json")
MAX_HISTORY = 20

class MemoryManager:
    def __init__(self):
        self.memory = {
            "last_opened_app": None,
            "last_executed_cmd": None,
            "action_frequency": {},
            "recent_history": [],
            "last_suggestion_time": 0,
            "pending_action": None,
            "pending_action_time": 0
        }
        self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    # Merge data gracefully to preserve defaults for missing keys
                    for k in self.memory:
                        if k in data:
                            self.memory[k] = data[k]
            except Exception as e:
                print("Failed to load memory:", e)

    def save_memory(self):
        # Ensure directory exists before writing
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        try:
            # Create a shallow copy without volatile vision state to save to disk
            disk_memory = self.memory.copy()
            if "vision_state" in disk_memory:
                del disk_memory["vision_state"]
                
            with open(MEMORY_FILE, "w") as f:
                json.dump(disk_memory, f, indent=4)
        except Exception as e:
            print("Failed to save memory:", e)

    def add_history(self, action, value, result):
        record = f"Action: {action} | Target: {value} | Result: {result}"
        self.memory["recent_history"].append(record)
        
        # Enforce size limit
        if len(self.memory["recent_history"]) > MAX_HISTORY:
            self.memory["recent_history"].pop(0)

        # Update action frequencies
        if action not in self.memory["action_frequency"]:
            self.memory["action_frequency"][action] = 0
        self.memory["action_frequency"][action] += 1

        self.memory["last_executed_cmd"] = action

        if action == "OPEN_APP":
            self.memory["last_opened_app"] = value
            
        self.save_memory()

    def add_conversation(self, text):
        self.memory["recent_history"].append(f"AI Replied Conversational: {text}")
        if len(self.memory["recent_history"]) > MAX_HISTORY:
            self.memory["recent_history"].pop(0)
        self.save_memory()

    def clear_memory(self):
        self.memory = {
            "last_opened_app": None,
            "last_executed_cmd": None,
            "action_frequency": {},
            "recent_history": [],
            "last_suggestion_time": 0,
            "pending_action": None,
            "pending_action_time": 0
        }
        self.save_memory()
        return "Memory completely erased."

    def can_suggest(self, cooldown_seconds=1800):
        """Returns True if enough time has passed since the last proactive suggestion."""
        last_time = self.memory.get("last_suggestion_time", 0)
        return (time.time() - last_time) > cooldown_seconds

    def update_suggestion_time(self):
        self.memory["last_suggestion_time"] = time.time()
        self.save_memory()

    def add_proactive_history(self, suggestion):
        self.memory["recent_history"].append(f"AI Proactively Suggested: {suggestion}")
        if len(self.memory["recent_history"]) > MAX_HISTORY:
            self.memory["recent_history"].pop(0)
        self.update_suggestion_time()

    def get_context_string(self):
        ctx = "--- STRUCTURED MEMORY LEVEL ---\n"
        ctx += f"LAST OPENED APP: {self.memory['last_opened_app']}\n"
        ctx += f"LAST EXECUTED COMMAND: {self.memory['last_executed_cmd']}\n"
        
        # Sort and show top 3 favorite commands
        sorted_freqs = sorted(self.memory['action_frequency'].items(), key=lambda x: x[1], reverse=True)
        favorites = ", ".join([f"{k} ({v}x)" for k, v in sorted_freqs[:3]])
        ctx += f"FAVORITE COMMANDS: {favorites if favorites else 'None yet'}\n"
        
        # Injects the active vision status without bloat
        vs = self.memory.get("vision_state")
        if vs:
            ctx += f"\n--- ACTIVE CAMERA VISION STATE ---\n"
            ctx += f"User Engagement: {vs.get('engagement', 'offline')}\n"
            ctx += f"Soft Detected Emotion: {vs.get('emotion', 'unknown')}\n"
        
        ctx += "\n--- SHORT TERM HISTORY (Oldest to Newest) ---\n"
        if not self.memory["recent_history"]:
            ctx += "No recent history.\n"
        else:
            for item in self.memory["recent_history"]:
                ctx += f"- {item}\n"
        return ctx

    def set_pending_action(self, action_list):
        self.memory["pending_action"] = action_list
        self.memory["pending_action_time"] = time.time()
        # We don't save_memory() here to keep it volatile and non-persistent across reboots

    def get_pending_action(self):
        return self.memory.get("pending_action")

    def get_pending_action_time(self):
        return self.memory.get("pending_action_time", 0)

    def clear_pending_action(self):
        self.memory["pending_action"] = None
        self.memory["pending_action_time"] = 0

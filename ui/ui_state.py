from enum import Enum

class UIState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    RESPONDING = "RESPONDING"

_current_state = UIState.IDLE
_last_user_text = ""
_last_ai_text = ""

def set_state(state: UIState):
    global _current_state
    _current_state = state

def set_user_text(text: str):
    global _last_user_text
    _last_user_text = text

def set_ai_text(text: str):
    global _last_ai_text
    _last_ai_text = text

def get_ui_data():
    return _current_state, _last_user_text, _last_ai_text

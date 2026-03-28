import threading
from security.face_auth import verify_face
from ui.jarvis_ui import start_ui

def start_auth(on_success):
    success = verify_face()

    if success:
        # 🔥 Start Jarvis in background thread
        jarvis_thread = threading.Thread(
            target=on_success,
            daemon=True
        )
        jarvis_thread.start()

        # UI MUST be on main thread
        start_ui()
    else:
        print("Authentication failed")

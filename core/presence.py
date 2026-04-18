import cv2
import time
import threading

class PresenceTracker:
    def __init__(self):
        self.is_running = False
        self.thread = None
        
        # Internal state tracking
        self.last_face_time = time.time()
        self.last_movement_time = time.time()
        self.first_no_face_time = None
        
        # State stability tracking
        self.proposed_state = "ACTIVE"
        self.proposed_state_time = time.time()
        self.confirmed_state = "ACTIVE"
        
        # Settings
        self.STATE_STABILITY_SEC = 5.0  # Must stay in proposed state for 5s to confirm
        self.IDLE_THRESHOLD_SEC = 60.0  # 60 seconds of low movement = IDLE
        self.MOTION_THRESHOLD = 500     # Pixels changed
        
    def get_state(self):
        """Returns the stable, confirmed state."""
        return self.confirmed_state
        
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            
    def _run_loop(self):
        cap = cv2.VideoCapture(0)
        # Small resolution for performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        window_name = 'Sara Presence'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 200, 150)
        # Always on top
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

        prev_gray = None
        
        while self.is_running:
            loop_start = time.time()
            ret, frame = cap.read()
            if not ret:
                time.sleep(1)
                continue
                
            frame = cv2.flip(frame, 1)
            display_frame = frame.copy()
            
            # 1. Processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Detect face
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            has_face = len(faces) > 0
            
            if has_face:
                # Draw box around largest face
                faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
                x, y, w, h = faces[0]
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Detect Movement
            is_moving = False
            if prev_gray is not None:
                frame_diff = cv2.absdiff(prev_gray, gray)
                thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                motion_pixels = cv2.countNonZero(thresh)
                
                if motion_pixels > self.MOTION_THRESHOLD:
                    is_moving = True
                    # Optional visualization of movement
                    cv2.putText(display_frame, f"MOTION: {motion_pixels}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            prev_gray = gray
            
            # 2. Update Internal Timers
            current_time = time.time()
            if has_face:
                self.last_face_time = current_time
                self.first_no_face_time = None
            else:
                if self.first_no_face_time is None:
                    self.first_no_face_time = current_time
            
            if is_moving and has_face:
                self.last_movement_time = current_time

            # 3. Determine proposed state
            # If no face detected for at least some initial raw threshold (e.g. 2s) to avoid blink misses
            new_proposed_state = "ACTIVE"
            
            if self.first_no_face_time and (current_time - self.first_no_face_time) > 2.0:
                new_proposed_state = "NO_FACE"
            else:
                if (current_time - self.last_movement_time) > self.IDLE_THRESHOLD_SEC:
                    new_proposed_state = "IDLE_WITH_FACE"
                else:
                    new_proposed_state = "ACTIVE"
                    
            # 4. State Stabilization (Must persist for STATE_STABILITY_SEC)
            if new_proposed_state != self.proposed_state:
                self.proposed_state = new_proposed_state
                self.proposed_state_time = current_time
            
            if self.proposed_state != self.confirmed_state:
                if (current_time - self.proposed_state_time) >= self.STATE_STABILITY_SEC:
                    # Transition confirmed
                    self.confirmed_state = self.proposed_state
                    print(f"👁️ Presence State Changed: {self.confirmed_state}")
            
            # UI Info
            cv2.putText(display_frame, f"STATE: {self.confirmed_state}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            cv2.imshow(window_name, display_frame)
            if cv2.waitKey(1) & 0xFF == 27:
                pass
                
            # Sleep 1-2 seconds (e.g. 1.0s) to keep CPU low
            # Calculate remaining time to sleep to maintain roughly 1s frequency
            elapsed = time.time() - loop_start
            sleep_time = max(0, 1.0 - elapsed)
            time.sleep(sleep_time)

        cap.release()
        cv2.destroyWindow(window_name)

# Global singleton
presence_tracker = PresenceTracker()

def start_presence():
    presence_tracker.start()
    
def stop_presence():
    presence_tracker.stop()
    
def get_user_state():
    return presence_tracker.get_state()

import cv2
import threading
import time

VISION_ACTIVE = False
vision_thread = None

# We use lightweight pre-trained Haar Cascades from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

def vision_loop(memory_manager):
    global VISION_ACTIVE
    
    # Init capture with extremely low overhead resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Floating window config
    window_name = 'Sara Vision'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 280, 200) # Small unassuming window
    # Keep always on top
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    frame_count = 0
    consecutive_no_face = 0
    consecutive_no_smile = 0
    
    # Initialize active state safely
    if "vision_state" not in memory_manager.memory:
        memory_manager.memory["vision_state"] = {}
        
    memory_manager.memory["vision_state"]["emotion"] = "neutral"
    memory_manager.memory["vision_state"]["engagement"] = "inactive"
    
    last_detect_box = None
    last_emotion = "neutral"

    while VISION_ACTIVE:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Process detection 1 time per 15 frames (approx 2 times a second)
        # Keeps UI smooth while minimizing CPU footprint
        if frame_count % 15 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # detect face
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                consecutive_no_face += 1
                if consecutive_no_face > 6:  # Approx 3 seconds of no face
                    last_emotion = "none"
                    memory_manager.memory["vision_state"]["engagement"] = "inactive"
                    memory_manager.memory["vision_state"]["emotion"] = "none"
                    last_detect_box = None
            else:
                consecutive_no_face = 0
                memory_manager.memory["vision_state"]["engagement"] = "active"
                
                # Assume largest face is the target user
                faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
                x, y, w, h = faces[0]
                last_detect_box = (x, y, w, h)
                
                roi_gray = gray[y:y+h, x:x+w]
                # detect soft smile expression
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                
                if len(smiles) > 0:
                    last_emotion = "happy"
                    consecutive_no_smile = 0
                else:
                    consecutive_no_smile += 1
                    # Soft diagnostic: if user has not smiled for approx 15 seconds, assume "sad" 
                    if consecutive_no_smile > 30:
                        last_emotion = "sad"
                    else:
                        last_emotion = "neutral"
                        
                memory_manager.memory["vision_state"]["emotion"] = last_emotion

        # Render loop (runs every frame to keep video playing smoothly like a mirror)
        display_frame = frame.copy()
        display_frame = cv2.flip(display_frame, 1) # Video mirror
        
        if last_detect_box:
            ox, oy, w, h = last_detect_box
            width = display_frame.shape[1]
            mx = width - ox - w  # Remap box X coordinate after flip
            
            color = (0, 255, 0) if last_emotion == "happy" else (0, 200, 255) if last_emotion == "neutral" else (0, 50, 255)
            cv2.rectangle(display_frame, (mx, oy), (mx+w, oy+h), color, 2)
            cv2.putText(display_frame, last_emotion.upper(), (mx, oy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        else:
            cv2.putText(display_frame, "INACTIVE", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
        cv2.imshow(window_name, display_frame)
        
        # 30ms sleep locks the thread to ~30 FPS max
        if cv2.waitKey(30) & 0xFF == 27:
            # Quit via ESC if the user manually tries to close the window
            break

    # Once VISION_ACTIVE is flipped false (via voice command or loop break)
    cap.release()
    cv2.destroyAllWindows()
    memory_manager.memory["vision_state"]["engagement"] = "inactive"

def start_vision(memory_manager):
    global VISION_ACTIVE, vision_thread
    if not VISION_ACTIVE:
        VISION_ACTIVE = True
        vision_thread = threading.Thread(target=vision_loop, args=(memory_manager,), daemon=True)
        vision_thread.start()
        return "Started the background vision system."
    return "Camera is already running."

def stop_vision():
    global VISION_ACTIVE
    if VISION_ACTIVE:
        VISION_ACTIVE = False
        return "Camera deactivated."
    return "Camera is already off."

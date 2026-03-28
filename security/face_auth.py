# import face_recognition
# import cv2

# OWNER_IMAGE = "data/owner.jpg"

# def verify_face():
#     known_image = face_recognition.load_image_file(OWNER_IMAGE)
#     known_encoding = face_recognition.face_encodings(known_image)[0]

#     cap = cv2.VideoCapture(0)

#     for _ in range(40):  # ~5 seconds
#         ret, frame = cap.read()
#         if not ret:
#             continue

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         faces = face_recognition.face_locations(rgb)
#         encodings = face_recognition.face_encodings(rgb, faces)

#         for encoding in encodings:
#             match = face_recognition.compare_faces(
#                 [known_encoding], encoding, tolerance=0.45
#             )
#             if match[0]:
#                 cap.release()
#                 cv2.destroyAllWindows()
#                 return True

#         cv2.imshow("Verifying Face...", frame)
#         if cv2.waitKey(1) & 0xFF == 27:
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return False


# TEMPORARY AUTH (NO face_recognition)

import cv2

def verify_face():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not opening")
        return False

    print("Camera opened. Press Q to exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Auth Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


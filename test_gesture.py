# test_gesture.py

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def get_finger_states(landmarks):
    fingers = []
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    tips = [8, 12, 16, 20]
    pip  = [6, 10, 14, 18]
    for tip, p in zip(tips, pip):
        if landmarks[tip].y < landmarks[p].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def classify(fingers):
    thumb, index, middle, ring, pinky = fingers

    if thumb == 1 and index == 1 and middle == 1 and ring == 1 and pinky == 1:
        return "OPEN PALM"
    if index == 1 and middle == 1 and ring == 0 and pinky == 0 and thumb == 0:
        return "PEACE SIGN"
    if index == 0 and middle == 0 and ring == 0 and pinky == 0 and thumb == 0:
        return "FIST"
    if index == 1 and middle == 0 and ring == 0 and pinky == 0 and thumb == 0:
        return "POINT UP"
    if index == 1 and middle == 1 and ring == 1 and pinky == 0 and thumb == 0:
        return "THREE FINGERS"
    return "UNKNOWN"

print("Testing gestures --- Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "UNKNOWN"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(hand_landmarks.landmark)
            gesture = classify(fingers)

    cv2.putText(frame, f"Gesture: {gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
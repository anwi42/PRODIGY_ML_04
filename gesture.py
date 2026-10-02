# gesture.py

import cv2
import mediapipe as mp
import config
import time
from collections import deque, namedtuple

Point = namedtuple("Point", ["x", "y"])

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.current_gesture = config.GESTURE_UNKNOWN
        self.confidence = 0.0

        # Hold timer
        self.hold_gesture = config.GESTURE_UNKNOWN
        self.hold_start_time = None
        self.gesture_confirmed = config.GESTURE_UNKNOWN
        self.hold_progress = 0.0  # 0.0 to 1.0
        self.hold_time = config.GESTURE_HOLD_TIME

        # Landmark smoothing — averages the last 3 frames to cut jitter
        self.landmark_history = deque(maxlen=3)

    def smooth_landmarks(self, landmarks):
        points = [(lm.x, lm.y) for lm in landmarks]
        self.landmark_history.append(points)

        n = len(self.landmark_history)
        smoothed = []
        for i in range(len(points)):
            avg_x = sum(frame[i][0] for frame in self.landmark_history) / n
            avg_y = sum(frame[i][1] for frame in self.landmark_history) / n
            smoothed.append(Point(avg_x, avg_y))
        return smoothed

    def get_finger_states(self, landmarks):
        fingers = []

        # Thumb
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Four fingers
        tips = [8, 12, 16, 20]
        pip  = [6, 10, 14, 18]
        for tip, p in zip(tips, pip):
            if landmarks[tip].y < landmarks[p].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers  # [thumb, index, middle, ring, pinky]

    def classify_gesture(self, fingers):
        thumb, index, middle, ring, pinky = fingers

        # Open Palm — all 5 fingers up
        if thumb == 1 and index == 1 and middle == 1 and ring == 1 and pinky == 1:
            return config.GESTURE_OPEN_PALM, 1.0

        # Peace Sign — only index and middle up
        if index == 1 and middle == 1 and ring == 0 and pinky == 0 and thumb == 0:
            return config.GESTURE_PEACE, 1.0

        # Fist — all fingers down
        if index == 0 and middle == 0 and ring == 0 and pinky == 0 and thumb == 0:
            return config.GESTURE_FIST, 1.0
            
        # Point Up — only index finger up
        if index == 1 and middle == 0 and ring == 0 and pinky == 0 and thumb == 0:
            return config.GESTURE_POINT_UP, 1.0

        

        return config.GESTURE_UNKNOWN, 0.0

    def update_hold_timer(self, gesture):
        if gesture == config.GESTURE_UNKNOWN:
            # Reset hold timer
            self.hold_gesture = config.GESTURE_UNKNOWN
            self.hold_start_time = None
            self.hold_progress = 0.0
            self.gesture_confirmed = config.GESTURE_UNKNOWN
            return config.GESTURE_UNKNOWN

        if gesture != self.hold_gesture:
            # New gesture detected — reset and start timing
            self.hold_gesture = gesture
            self.hold_start_time = time.time()
            self.hold_progress = 0.0
            self.gesture_confirmed = config.GESTURE_UNKNOWN
            return config.GESTURE_UNKNOWN

        # Same gesture held — check duration
        elapsed = time.time() - self.hold_start_time
        self.hold_progress = min(elapsed / self.hold_time, 1.0)

        if elapsed >= self.hold_time:
            self.gesture_confirmed = gesture
            # Reset so it doesnt keep firing
            self.hold_start_time = time.time()
            self.hold_progress = 0.0
            return gesture

        return config.GESTURE_UNKNOWN

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, config.GESTURE_UNKNOWN, 0.0, 0.0

        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        raw_gesture = config.GESTURE_UNKNOWN
        confidence = 0.0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                smoothed = self.smooth_landmarks(hand_landmarks.landmark)
                fingers = self.get_finger_states(smoothed)
                raw_gesture, confidence = self.classify_gesture(fingers)
        else:
            self.landmark_history.clear()

        confirmed_gesture = self.update_hold_timer(raw_gesture)
        self.current_gesture = raw_gesture
        self.confidence = confidence

        return frame, confirmed_gesture, raw_gesture, self.hold_progress

    def release(self):
        self.cap.release()
# modes/speedrush.py

import time
import config

class SpeedRushMode:
    def __init__(self, detector):
        self.detector = detector
        self.reset()

    def reset(self):
        self.score = 0
        self.flowers_bloomed = 0
        self.time_left = config.SPEEDRUSH_TIME_LIMIT
        self.hold_time = config.SPEEDRUSH_START_HOLD_TIME
        self.speed_multiplier = 1.0
        self.elapsed_total = 0.0
        self.last_time = time.time()
        self.game_over = False
        self.detector.hold_time = self.hold_time

    def update_hold_time(self):
        steps = int(self.elapsed_total // config.SPEEDRUSH_SPEEDUP_INTERVAL)
        new_hold = config.SPEEDRUSH_START_HOLD_TIME - \
            steps * config.SPEEDRUSH_HOLD_DECREASE
        self.hold_time = max(config.SPEEDRUSH_MIN_HOLD_TIME, new_hold)
        self.speed_multiplier = round(
            config.SPEEDRUSH_START_HOLD_TIME / self.hold_time, 2)
        self.detector.hold_time = self.hold_time

    def update_score(self):
        self.score = round(self.flowers_bloomed * self.speed_multiplier)

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            if flower.is_complete():
                self.flowers_bloomed += 1
                self.update_score()
                flower.reset(cycle_color=True)
            return True
        else:
            self.time_left -= config.SPEEDRUSH_MISS_PENALTY
        return False

    def update(self, confirmed_gesture, flower):
        if self.game_over:
            return

        self.process_gesture(confirmed_gesture, flower)

        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now
        self.elapsed_total += elapsed
        self.time_left -= elapsed

        self.update_hold_time()
        self.update_score()

        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

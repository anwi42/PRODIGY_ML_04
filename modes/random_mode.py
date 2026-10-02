# modes/random_mode.py

import time
import random
import config

ALL_GESTURES = [
    config.GESTURE_OPEN_PALM,
    config.GESTURE_PEACE,
    config.GESTURE_FIST,
    config.GESTURE_POINT_UP,
]


class RandomMode:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.flowers_bloomed = 0
        self.time_left = config.RANDOM_TIME_LIMIT
        self.last_time = time.time()
        self.game_over = False

        self.current_stage = None
        self.override_gesture = None
        self.pending_gesture = None
        self.change_at = None
        self.swap_time = None

    def is_warning_active(self):
        return self.change_at is not None and self.override_gesture is None

    def maybe_schedule_change(self, flower):
        if self.current_stage == flower.stage:
            return
        self.current_stage = flower.stage
        self.override_gesture = None
        self.pending_gesture = None
        self.change_at = None

        if random.random() < config.RANDOM_CHANGE_CHANCE:
            required = flower.get_required_gesture()
            choices = [g for g in ALL_GESTURES if g != required]
            self.pending_gesture = random.choice(choices)
            self.change_at = time.time() + config.RANDOM_WARNING_TIME

    def get_required_gesture(self, flower):
        if self.override_gesture:
            return self.override_gesture
        return flower.get_required_gesture()

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        required = self.get_required_gesture(flower)
        if gesture == required:
            adapted_quickly = (
                self.swap_time is not None and
                time.time() - self.swap_time <= config.RANDOM_ADAPT_WINDOW
            )
            flower.advance_stage()
            self.score += config.RANDOM_POINTS_PER_FLOWER
            if adapted_quickly:
                self.score += config.RANDOM_ADAPT_BONUS
            self.swap_time = None
            self.override_gesture = None
            self.pending_gesture = None
            self.change_at = None

            if flower.is_complete():
                self.flowers_bloomed += 1
                flower.reset(cycle_color=True)
                self.current_stage = None
            else:
                self.current_stage = flower.stage
            return True
        return False

    def update(self, confirmed_gesture, flower):
        if self.game_over:
            return

        self.maybe_schedule_change(flower)

        if self.change_at is not None and self.override_gesture is None:
            if time.time() >= self.change_at:
                self.override_gesture = self.pending_gesture
                self.pending_gesture = None
                self.change_at = None
                self.swap_time = time.time()

        self.process_gesture(confirmed_gesture, flower)

        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now
        self.time_left -= elapsed
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

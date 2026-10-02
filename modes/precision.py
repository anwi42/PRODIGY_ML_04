# modes/precision.py

import config


class PrecisionMode:
    def __init__(self, detector):
        self.detector = detector
        self.reset()

    def reset(self):
        self.score = 0
        self.flowers_bloomed = 0
        self.streak = 0
        self.wilts = 0
        self.game_over = False
        self.detector.hold_time = config.PRECISION_GESTURE_WINDOW

    def get_multiplier(self):
        if self.streak >= config.PRECISION_STREAK_TIER2:
            return config.PRECISION_MULTIPLIER_TIER2
        elif self.streak >= config.PRECISION_STREAK_TIER1:
            return config.PRECISION_MULTIPLIER_TIER1
        return 1

    def update_score(self):
        self.score = self.flowers_bloomed * self.get_multiplier()

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            self.streak += 1
            if flower.is_complete():
                self.flowers_bloomed += 1
                flower.reset(cycle_color=True)
            self.update_score()
            return True
        else:
            flower.wilt()
            self.streak = 0
            self.wilts += 1
            self.update_score()
            if self.wilts >= config.PRECISION_MAX_WILTS:
                self.game_over = True
        return False

    def update(self, confirmed_gesture, flower):
        if self.game_over:
            return
        self.process_gesture(confirmed_gesture, flower)

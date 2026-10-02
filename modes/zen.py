# modes/zen.py

import random
import config

class ZenMode:
    def __init__(self):
        self.reset()

    def reset(self):
        self.flowers_bloomed = 0

    def process_gesture(self, gesture, flower):
        if gesture == config.GESTURE_UNKNOWN:
            return False

        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            if flower.is_complete():
                self.flowers_bloomed += 1
                flower.reset()
                flower.color = random.choice(config.FLOWER_COLORS)
            return True
        return False

    def update(self, confirmed_gesture, flower):
        self.process_gesture(confirmed_gesture, flower)

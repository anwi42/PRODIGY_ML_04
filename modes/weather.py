# modes/weather.py

import time
import random
import config

WEATHER_RAIN = "rain"
WEATHER_WIND = "wind"


class WeatherMode:
    def __init__(self, detector):
        self.detector = detector
        self.reset()

    def reset(self):
        self.score = 0
        self.flowers_bloomed = 0
        self.time_left = config.WEATHER_TIME_LIMIT
        self.last_time = time.time()
        self.game_over = False
        self.win = False

        self.elapsed_total = 0.0
        self.next_weather_at = config.WEATHER_EVENT_INTERVAL

        self.weather_event = None
        self.weather_timer = 0.0
        self.shake_offset = (0, 0)

        self.base_hold_time = config.GESTURE_HOLD_TIME
        self.detector.hold_time = self.base_hold_time

    @property
    def weather_time_remaining(self):
        if not self.weather_event:
            return 0.0
        return max(0.0, config.WEATHER_EVENT_DURATION - self.weather_timer)

    def trigger_weather(self):
        self.weather_event = random.choice([WEATHER_RAIN, WEATHER_WIND])
        self.weather_timer = 0.0
        if self.weather_event == WEATHER_RAIN:
            self.detector.hold_time = \
                self.base_hold_time * (1 + config.WEATHER_RAIN_SLOWDOWN)
        else:
            self.detector.hold_time = max(
                config.SPEEDRUSH_MIN_HOLD_TIME,
                self.base_hold_time * config.WEATHER_WIND_SHRINK)

    def clear_weather(self):
        self.weather_event = None
        self.weather_timer = 0.0
        self.shake_offset = (0, 0)
        self.detector.hold_time = self.base_hold_time

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        # Clearing gesture for the active weather event
        if self.weather_event == WEATHER_RAIN and \
                gesture == config.GESTURE_OPEN_PALM:
            self.clear_weather()
        elif self.weather_event == WEATHER_WIND and \
                gesture == config.GESTURE_FIST:
            self.clear_weather()

        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            if flower.is_complete():
                self.flowers_bloomed += 1
                self.score += config.WEATHER_POINTS_PER_FLOWER
                if self.flowers_bloomed >= config.WEATHER_FLOWER_TARGET:
                    self.win = True
                    self.game_over = True
                    self.clear_weather()
                else:
                    flower.reset(cycle_color=True)
            return True
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

        if self.weather_event:
            self.weather_timer += elapsed
            if self.weather_event == WEATHER_WIND:
                shake = config.WEATHER_SHAKE_PIXELS
                self.shake_offset = (
                    random.randint(-shake, shake),
                    random.randint(-shake, shake))
            if self.weather_timer >= config.WEATHER_EVENT_DURATION:
                self.clear_weather()
        elif self.elapsed_total >= self.next_weather_at:
            self.trigger_weather()
            self.next_weather_at += config.WEATHER_EVENT_INTERVAL

        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            self.clear_weather()

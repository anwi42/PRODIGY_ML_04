# game.py

import time
import random
import config

class Game:
    def __init__(self):
        self.level = 1
        self.reset()

    def reset(self):
        # Common
        self.score = 0
        self.flowers_bloomed = 0
        self.running = True
        self.game_over = False
        self.level_complete = False

        # Timed Bloom (level 1)
        self.time_left = config.TIMED_BLOOM_TIME_LIMIT
        self.last_time = time.time()
        self.current_color_name = "pink"
        self.targets = {}
        self.collection = {}
        self.timed_bloom_started = False

        # Survival (level 2)
        self.lives = config.SURVIVAL_LIVES
        self.survival_time_left = config.SURVIVAL_TIME_LIMIT
        self.survival_last_time = time.time()
        self.danger_mode = False
        self.current_plant_type = "flower"
        self.stage_timer = 0.0
        self.stage_time_limit = config.SURVIVAL_EASY_RESPONSE
        self.stage_last_time = time.time()
        self.waiting_on_weed = False
        self.weed_timer = 0.0
        self.weed_wait_time = 3.0

    def set_level(self, level):
        self.level = level
        self.reset()
        if level == 1:
            self.generate_timed_bloom_targets()

    def generate_timed_bloom_targets(self):
        # Pick only 3 random colors out of 4 as targets
        all_colors = list(config.TIMED_BLOOM_FLOWER_COLORS.keys())
        chosen_colors = random.sample(all_colors, 3)
        self.targets = {}
        self.collection = {}
        for color_name in chosen_colors:
            self.targets[color_name] = random.randint(1, 3)
            self.collection[color_name] = 0

    def get_needed_colors(self):
        # Returns list of colors where collection < target
        needed = []
        for color_name in self.targets:
            if self.collection[color_name] < self.targets[color_name]:
                needed.append(color_name)
        return needed

    def all_targets_met(self):
        for color_name in self.targets:
            if self.collection[color_name] < self.targets[color_name]:
                return False
        return True

    def spawn_timed_bloom_flower(self, flower):
        needed = self.get_needed_colors()

        if not needed:
            return

        # Dynamic probability based on time left
        if self.time_left <= config.TIMED_BLOOM_LATE_THRESHOLD:
            needed_chance = config.TIMED_BLOOM_NEEDED_CHANCE_LATE
        else:
            needed_chance = config.TIMED_BLOOM_NEEDED_CHANCE_EARLY

        roll = random.random()

        if roll < needed_chance:
            # Spawn a needed color
            chosen = random.choice(needed)
        else:
            # Spawn any random color
            chosen = random.choice(
                list(config.TIMED_BLOOM_FLOWER_COLORS.keys()))

        self.current_color_name = chosen
        flower.reset()
        flower.color = config.TIMED_BLOOM_FLOWER_COLORS[chosen]

    def get_survival_response_time(self):
        elapsed = config.SURVIVAL_TIME_LIMIT - self.survival_time_left
        if elapsed < 30:
            return config.SURVIVAL_EASY_RESPONSE
        elif elapsed < 60:
            return config.SURVIVAL_MEDIUM_RESPONSE
        else:
            return config.SURVIVAL_HARD_RESPONSE

    def spawn_next_plant(self, flower):
        roll = random.random()
        if roll < config.SURVIVAL_WEED_CHANCE:
            self.current_plant_type = "weed"
            flower.reset()
            flower.set_weed()
            self.waiting_on_weed = True
            self.weed_timer = 0.0
        elif roll < config.SURVIVAL_WEED_CHANCE + config.SURVIVAL_GOLDEN_CHANCE:
            self.current_plant_type = "golden"
            flower.reset()
            flower.set_golden()
            self.waiting_on_weed = False
        else:
            self.current_plant_type = "flower"
            flower.reset()
            self.waiting_on_weed = False

        self.stage_time_limit = self.get_survival_response_time()
        self.stage_last_time = time.time()

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        if self.level == 1:
            return self.process_gesture_timed_bloom(gesture, flower)
        elif self.level == 2:
            return self.process_gesture_survival(gesture, flower)

        return False

    def process_gesture_timed_bloom(self, gesture, flower):
        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            if flower.is_complete():
                self.flowers_bloomed += 1
                # Only add to collection if color is a target
                if self.current_color_name in self.collection:
                    self.collection[self.current_color_name] += 1
                self.score += 10

                # Check if all targets met
                if self.all_targets_met():
                    # Bonus points for remaining time
                    self.score += int(self.time_left) * \
                                  config.TIMED_BLOOM_BONUS_PER_SECOND
                    self.level_complete = True
                    self.game_over = True
                else:
                    self.spawn_timed_bloom_flower(flower)
            return True
        return False

    def process_gesture_survival(self, gesture, flower):
        if self.waiting_on_weed:
            self.lives -= 1
            self.waiting_on_weed = False
            if self.lives <= 0:
                self.game_over = True
            self.danger_mode = self.lives == 1
            self.spawn_next_plant(flower)
            return False

        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            self.stage_last_time = time.time()
            if flower.is_complete():
                self.flowers_bloomed += 1
                if self.current_plant_type == "golden":
                    self.score += config.SURVIVAL_GOLDEN_POINTS
                else:
                    self.score += config.SURVIVAL_POINTS_PER_FLOWER
                self.spawn_next_plant(flower)
            return True
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.danger_mode = self.lives == 1
        return False

    def update_timed_bloom_timer(self):
        if self.game_over:
            return
        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now
        self.time_left -= elapsed
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

    def update_survival(self, flower):
        if self.game_over:
            return

        now = time.time()
        elapsed = now - self.survival_last_time
        self.survival_last_time = now
        self.survival_time_left -= elapsed

        if self.survival_time_left <= 0:
            self.survival_time_left = 0
            self.game_over = True
            return

        self.danger_mode = self.lives == 1

        if self.waiting_on_weed:
            self.weed_timer += elapsed
            if self.weed_timer >= self.weed_wait_time:
                self.waiting_on_weed = False
                self.spawn_next_plant(flower)
            return

        stage_elapsed = now - self.stage_last_time
        self.stage_time_limit = self.get_survival_response_time()

        if stage_elapsed >= self.stage_time_limit:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.danger_mode = self.lives == 1
            self.spawn_next_plant(flower)

    def update(self, confirmed_gesture, flower):
        self.process_gesture(confirmed_gesture, flower)

        if self.level == 1:
            # Spawn first flower for Timed Bloom
            if not self.timed_bloom_started:
                self.spawn_timed_bloom_flower(flower)
                self.timed_bloom_started = True
            self.update_timed_bloom_timer()
        elif self.level == 2:
            self.update_survival(flower)

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

        # Level 1
        self.streak = 0

        # Level 2
        self.time_left = config.LEVEL2_TIME_LIMIT
        self.last_time = time.time()
        self.current_color_name = "pink"
        self.targets = {}
        self.collection = {}
        self.level2_started = False

        # Level 3
        self.lives = config.LEVEL3_LIVES
        self.level3_time_left = config.LEVEL3_TIME_LIMIT
        self.level3_last_time = time.time()
        self.danger_mode = False
        self.current_plant_type = "flower"
        self.stage_timer = 0.0
        self.stage_time_limit = config.LEVEL3_EASY_RESPONSE
        self.stage_last_time = time.time()
        self.waiting_on_weed = False
        self.weed_timer = 0.0
        self.weed_wait_time = 3.0

    def set_level(self, level):
        self.level = level
        self.reset()
        if level == 2:
            self.generate_level2_targets()

    def generate_level2_targets(self):
        # Pick only 3 random colors out of 4 as targets
        all_colors = list(config.LEVEL2_FLOWER_COLORS.keys())
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

    def spawn_level2_flower(self, flower):
        needed = self.get_needed_colors()

        if not needed:
            return

        # Dynamic probability based on time left
        if self.time_left <= config.LEVEL2_LATE_THRESHOLD:
            needed_chance = config.LEVEL2_NEEDED_CHANCE_LATE
        else:
            needed_chance = config.LEVEL2_NEEDED_CHANCE_EARLY

        roll = random.random()

        if roll < needed_chance:
            # Spawn a needed color
            chosen = random.choice(needed)
        else:
            # Spawn any random color
            chosen = random.choice(
                list(config.LEVEL2_FLOWER_COLORS.keys()))

        self.current_color_name = chosen
        flower.reset()
        flower.color = config.LEVEL2_FLOWER_COLORS[chosen]

    def get_level3_response_time(self):
        elapsed = config.LEVEL3_TIME_LIMIT - self.level3_time_left
        if elapsed < 30:
            return config.LEVEL3_EASY_RESPONSE
        elif elapsed < 60:
            return config.LEVEL3_MEDIUM_RESPONSE
        else:
            return config.LEVEL3_HARD_RESPONSE

    def spawn_next_plant(self, flower):
        roll = random.random()
        if roll < config.LEVEL3_WEED_CHANCE:
            self.current_plant_type = "weed"
            flower.reset()
            flower.set_weed()
            self.waiting_on_weed = True
            self.weed_timer = 0.0
        elif roll < config.LEVEL3_WEED_CHANCE + config.LEVEL3_GOLDEN_CHANCE:
            self.current_plant_type = "golden"
            flower.reset()
            flower.set_golden()
            self.waiting_on_weed = False
        else:
            self.current_plant_type = "flower"
            flower.reset()
            self.waiting_on_weed = False

        self.stage_time_limit = self.get_level3_response_time()
        self.stage_last_time = time.time()

    def process_gesture(self, gesture, flower):
        if self.game_over:
            return False
        if gesture == config.GESTURE_UNKNOWN:
            return False

        if self.level == 1:
            return self.process_gesture_level1(gesture, flower)
        elif self.level == 2:
            return self.process_gesture_level2(gesture, flower)
        elif self.level == 3:
            return self.process_gesture_level3(gesture, flower)

        return False

    def process_gesture_level1(self, gesture, flower):
        required = flower.get_required_gesture()
        if gesture == required:
            flower.advance_stage()
            if flower.is_complete():
                self.flowers_bloomed += 1
                self.streak += 1
                if self.flowers_bloomed >= config.LEVEL1_FLOWER_TARGET:
                    self.game_over = True
                else:
                    flower.reset(cycle_color=True)
            return True
        else:
            self.streak = 0
        return False

    def process_gesture_level2(self, gesture, flower):
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
                                  config.LEVEL2_BONUS_PER_SECOND
                    self.level_complete = True
                    self.game_over = True
                else:
                    self.spawn_level2_flower(flower)
            return True
        return False

    def process_gesture_level3(self, gesture, flower):
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
                    self.score += config.LEVEL3_GOLDEN_POINTS
                else:
                    self.score += config.LEVEL3_POINTS_PER_FLOWER
                self.spawn_next_plant(flower)
            return True
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.danger_mode = self.lives == 1
        return False

    def update_level2_timer(self):
        if self.game_over:
            return
        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now
        self.time_left -= elapsed
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

    def update_level3(self, flower):
        if self.game_over:
            return

        now = time.time()
        elapsed = now - self.level3_last_time
        self.level3_last_time = now
        self.level3_time_left -= elapsed

        if self.level3_time_left <= 0:
            self.level3_time_left = 0
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
        self.stage_time_limit = self.get_level3_response_time()

        if stage_elapsed >= self.stage_time_limit:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.danger_mode = self.lives == 1
            self.spawn_next_plant(flower)

    def update(self, confirmed_gesture, flower):
        self.process_gesture(confirmed_gesture, flower)

        if self.level == 2:
            # Spawn first flower for level 2
            if not self.level2_started:
                self.spawn_level2_flower(flower)
                self.level2_started = True
            self.update_level2_timer()
        elif self.level == 3:
            self.update_level3(flower)
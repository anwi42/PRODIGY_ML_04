# ui.py

import pygame
import config

class UI:
    GESTURE_NAMES = {
        config.GESTURE_OPEN_PALM: "Open Palm",
        config.GESTURE_PEACE:     "Peace Sign",
        config.GESTURE_FIST:      "Fist",
        config.GESTURE_POINT_UP:  "Point Up",
        config.GESTURE_UNKNOWN:   "No Gesture",
    }

    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Arial", config.FONT_LARGE, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", config.FONT_MEDIUM)
        self.font_small = pygame.font.SysFont("Arial", config.FONT_SMALL)
        self.font_tiny = pygame.font.SysFont("Arial", config.FONT_TINY)
        self.leaderboard = []

        # Load menu background image
        try:
            self.menu_bg = pygame.image.load("menu_bg.jpg")
            self.menu_bg = pygame.transform.scale(
                self.menu_bg,
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except:
            self.menu_bg = None

    def draw_text_centered(self, text, font, color, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(config.SCREEN_WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_bg_with_overlay(self, overlay_alpha=80):
        if self.menu_bg:
            self.screen.blit(self.menu_bg, (0, 0))
            overlay = pygame.Surface(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
                pygame.SRCALPHA)
            overlay.fill((0, 0, 0, overlay_alpha))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((5, 15, 5))

    def draw_background(self, danger=False, zen=False):
        if zen:
            self.screen.fill(config.ZEN_BG_COLOR)
        elif danger:
            self.screen.fill((40, 10, 10))
        else:
            self.screen.fill((10, 10, 15))

        # Subtle bottom ground
        pygame.draw.rect(self.screen, (20, 35, 20),
                         (0, config.SCREEN_HEIGHT - 60,
                          config.SCREEN_WIDTH, 60))

        # Decorative trees
        tree_positions = [80, 220, 420, 680, 900, 1100, 1220]
        for tx in tree_positions:
            pygame.draw.rect(self.screen, (40, 25, 10),
                             (tx - 6, config.SCREEN_HEIGHT - 110, 12, 60))
            pygame.draw.circle(self.screen, (15, 40, 15),
                               (tx, config.SCREEN_HEIGHT - 130), 35)
            pygame.draw.circle(self.screen, (20, 50, 20),
                               (tx - 18, config.SCREEN_HEIGHT - 115), 25)
            pygame.draw.circle(self.screen, (20, 50, 20),
                               (tx + 18, config.SCREEN_HEIGHT - 115), 25)

    def draw_landing(self):
        # Background with light overlay
        self.draw_bg_with_overlay(overlay_alpha=80)

        # Top and bottom gold accent bars
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, 0, config.SCREEN_WIDTH, 3))
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, config.SCREEN_HEIGHT - 3,
                          config.SCREEN_WIDTH, 3))

        # Title
        title_font = pygame.font.SysFont("Georgia", 92, bold=True)

        # Shadow behind title
        shadow = title_font.render("PETAL RUSH", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(
            center=(config.SCREEN_WIDTH // 2 + 3,
                    config.SCREEN_HEIGHT // 2 - 30 + 3))
        self.screen.blit(shadow, shadow_rect)

        # Main title in white
        title = title_font.render("PETAL RUSH", True, config.WHITE)
        title_rect = title.get_rect(
            center=(config.SCREEN_WIDTH // 2,
                    config.SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(title, title_rect)

        # Thin gold line under title
        pygame.draw.rect(self.screen, config.GOLD,
                         (config.SCREEN_WIDTH // 2 - 180,
                          config.SCREEN_HEIGHT // 2 + 35,
                          360, 1))

        # Tagline
        tag_font = pygame.font.SysFont("Arial", 18)
        tag = tag_font.render(
            "Real-Time Hand Gesture Flower Blooming Game",
            True, (200, 200, 200))
        tag_rect = tag.get_rect(
            center=(config.SCREEN_WIDTH // 2,
                    config.SCREEN_HEIGHT // 2 + 55))
        self.screen.blit(tag, tag_rect)

        # Press enter text at bottom
        enter_font = pygame.font.SysFont("Arial", 16)
        enter = enter_font.render(
            "Press  ENTER  to continue",
            True, (160, 160, 160))
        enter_rect = enter.get_rect(
            center=(config.SCREEN_WIDTH // 2,
                    config.SCREEN_HEIGHT - 30))
        self.screen.blit(enter, enter_rect)

    def draw_menu(self):
        # Background with light overlay
        self.draw_bg_with_overlay(overlay_alpha=80)

        # Top and bottom gold accent bars
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, 0, config.SCREEN_WIDTH, 3))
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, config.SCREEN_HEIGHT - 3,
                          config.SCREEN_WIDTH, 3))

        # Title small at top
        small_title_font = pygame.font.SysFont("Georgia", 32, bold=True)
        small_title = small_title_font.render("PETAL RUSH", True, config.WHITE)
        small_title_rect = small_title.get_rect(
            center=(config.SCREEN_WIDTH // 2, 32))
        self.screen.blit(small_title, small_title_rect)

        # Thin gold divider under small title
        pygame.draw.rect(self.screen, (80, 60, 0),
                         (config.SCREEN_WIDTH // 2 - 200,
                          54, 400, 1))

        # Select level heading
        select_font = pygame.font.SysFont("Arial", 15, bold=True)
        select = select_font.render("SELECT A MODE", True, config.GOLD)
        select_rect = select.get_rect(
            center=(config.SCREEN_WIDTH // 2, 74))
        self.screen.blit(select, select_rect)

        # Mode cards — 2 column grid, 4 rows
        modes = [
            ("1", "Timed Bloom",
             "Complete the collection target before 60 seconds runs out.",
             (180, 140, 0)),
            ("2", "Survival Mode",
             "90 sec. 3 lives. Weeds. Speed increases over time.",
             (180, 60, 60)),
            ("3", "Zen Garden",
             "No timer, no pressure. Bloom flowers forever.",
             (80, 160, 200)),
            ("4", "Speed Rush",
             "60 sec. Gestures get faster every 10 seconds.",
             (200, 100, 180)),
            ("5", "Weather",
             "90 sec. Bloom 5. Clear Rain/Wind events as they hit.",
             (90, 150, 220)),
            ("6", "Precision",
             "0.5s gesture window. Build streak, avoid 3 wilts.",
             (220, 170, 60)),
            ("7", "Mirror Mode",
             "Timed Bloom rules — but your webcam feed is reversed.",
             (140, 110, 220)),
            ("8", "Random",
             "Required gestures randomly swap. Adapt fast for bonus.",
             (90, 190, 120)),
        ]

        col_w = 580
        card_h = 108
        row_spacing = 120
        gap = 40
        group_w = col_w * 2 + gap
        left_x = (config.SCREEN_WIDTH - group_w) // 2
        right_x = left_x + col_w + gap
        row_y_start = 100

        for i, (num, name, desc, accent) in enumerate(modes):
            row = i // 2
            col = i % 2
            card_x = left_x if col == 0 else right_x
            card_y = row_y_start + row * row_spacing

            # Card background — semi transparent
            card_surf = pygame.Surface((col_w, card_h), pygame.SRCALPHA)
            card_surf.fill((0, 0, 0, 160))
            self.screen.blit(card_surf, (card_x, card_y))

            # Card border
            pygame.draw.rect(self.screen, (40, 60, 40),
                             (card_x, card_y, col_w, card_h),
                             1, border_radius=8)

            # Left accent bar
            pygame.draw.rect(self.screen, accent,
                             (card_x, card_y, 4, card_h),
                             border_radius=8)

            # Mode number
            num_font = pygame.font.SysFont("Georgia", 32, bold=True)
            num_txt = num_font.render(num, True, accent)
            self.screen.blit(num_txt, (card_x + 18, card_y + 32))

            # Vertical divider
            pygame.draw.rect(self.screen, (50, 70, 50),
                             (card_x + 56, card_y + 14, 1, card_h - 28))

            # Mode name
            name_font = pygame.font.SysFont("Arial", 19, bold=True)
            name_txt = name_font.render(name, True, config.WHITE)
            self.screen.blit(name_txt, (card_x + 70, card_y + 20))

            # Description
            desc_font = pygame.font.SysFont("Arial", 12)
            desc_txt = desc_font.render(desc, True, (180, 180, 160))
            self.screen.blit(desc_txt, (card_x + 70, card_y + 52))

        # Bottom instruction
        inst_font = pygame.font.SysFont("Arial", 15)
        inst = inst_font.render(
            "Press  1 - 8  to begin",
            True, (160, 160, 160))
        inst_rect = inst.get_rect(
            center=(config.SCREEN_WIDTH // 2,
                    config.SCREEN_HEIGHT - 20))
        self.screen.blit(inst, inst_rect)

    def draw_gesture_prompt(self, gesture_needed, raw_gesture,
                            hold_progress):
        needed_name = self.GESTURE_NAMES.get(gesture_needed, "")
        current_name = self.GESTURE_NAMES.get(raw_gesture, "No Gesture")

        pygame.draw.rect(self.screen, (20, 20, 28),
                         (20, 20, 360, 95), border_radius=10)
        pygame.draw.rect(self.screen, config.GOLD,
                         (20, 20, 360, 95), 2, border_radius=10)

        self.draw_text("Do:", self.font_tiny, (150, 150, 150), 35, 28)
        self.draw_text(needed_name, self.font_medium, config.GOLD, 35, 50)
        self.draw_text(f"Detected: {current_name}",
                       self.font_tiny, (180, 180, 180), 35, 92)

    def draw_weed_prompt(self):
        pygame.draw.rect(self.screen, (20, 20, 28),
                         (20, 20, 360, 95), border_radius=10)
        pygame.draw.rect(self.screen, (200, 50, 50),
                         (20, 20, 360, 95), 2, border_radius=10)
        self.draw_text("WARNING!", self.font_tiny,
                       (200, 50, 50), 35, 28)
        self.draw_text("Do Nothing!", self.font_medium,
                       (200, 50, 50), 35, 50)
        self.draw_text("It's a Weed — any gesture loses a life",
                       self.font_tiny, (180, 180, 180), 35, 92)

    def draw_level1_hud(self, time_left, score, targets,
                        collection):
        # Timer
        self.draw_text(f"Time: {int(time_left)}s",
                       self.font_medium, config.WHITE, 20, 130)

        # Score
        self.draw_text(f"Score: {score}",
                       self.font_small, config.GOLD, 20, 180)

        # Collection panel on right side
        panel_x = config.SCREEN_WIDTH - 220
        panel_y = 220

        pygame.draw.rect(self.screen, (14, 35, 14),
                         (panel_x - 10, panel_y - 10,
                          210, 160), border_radius=8)
        pygame.draw.rect(self.screen, config.GOLD,
                         (panel_x - 10, panel_y - 10,
                          210, 160), 1, border_radius=8)

        self.draw_text("COLLECTION TARGET",
                       self.font_tiny, config.GOLD,
                       panel_x, panel_y)

        pygame.draw.rect(self.screen, (40, 60, 40),
                         (panel_x - 10, panel_y + 20,
                          210, 1))

        color_map = {
            "pink":   (255, 105, 180),
            "yellow": (255, 220, 50),
            "white":  (240, 240, 240),
            "red":    (220, 50, 50),
        }

        for i, (color_name, target) in enumerate(targets.items()):
            current = collection.get(color_name, 0)
            y = panel_y + 35 + i * 30

            pygame.draw.circle(self.screen,
                               color_map[color_name],
                               (panel_x + 8, y + 8), 8)

            self.draw_text(color_name.capitalize(),
                           self.font_tiny, config.WHITE,
                           panel_x + 24, y)

            count_color = (50, 200, 50) \
                if current >= target else config.WHITE
            count_txt = f"{current} / {target}"
            self.draw_text(count_txt, self.font_tiny,
                           count_color,
                           panel_x + 130, y)

            if current >= target:
                self.draw_text("✓", self.font_tiny,
                               (50, 200, 50),
                               panel_x + 185, y)

    def draw_level2_hud(self, lives, score, time_left,
                        flowers_bloomed, response_time):
        self.draw_text(f"Time: {int(time_left)}s",
                       self.font_medium, config.WHITE, 20, 130)

        lives_text = "Lives: " + "♥ " * lives
        self.draw_text(lives_text, self.font_small,
                       (200, 50, 50), 20, 180)

        self.draw_text(f"Score: {score}",
                       self.font_small, config.GOLD, 20, 215)

        self.draw_text(f"Flowers: {flowers_bloomed}",
                       self.font_small, config.WHITE, 20, 250)

        if time_left > 60:
            phase = "Easy  —  4s per stage"
            phase_color = (50, 200, 50)
        elif time_left > 30:
            phase = "Medium  —  3s per stage"
            phase_color = (255, 165, 0)
        else:
            phase = "Hard  —  2s per stage"
            phase_color = (200, 50, 50)

        self.draw_text(phase, self.font_tiny,
                       phase_color, 20, 285)

    def draw_zen_hud(self, flowers_bloomed):
        self.draw_text(f"Flowers Bloomed: {flowers_bloomed}",
                       self.font_small, config.WHITE, 20, 130)

    def draw_speedrush_hud(self, time_left, speed_multiplier,
                           flowers_bloomed):
        self.draw_text(f"Time: {int(time_left)}s",
                       self.font_medium, config.WHITE, 20, 130)
        self.draw_text(f"Speed: x{speed_multiplier}",
                       self.font_small, config.GOLD, 20, 180)
        self.draw_text(f"Flowers: {flowers_bloomed}",
                       self.font_small, config.WHITE, 20, 215)

    def draw_weather_hud(self, time_left, flowers_bloomed,
                         weather_event, weather_time_remaining):
        self.draw_text(f"Time: {int(time_left)}s",
                       self.font_medium, config.WHITE, 20, 130)
        self.draw_text(f"Flowers: {flowers_bloomed} / 5",
                       self.font_small, config.GOLD, 20, 180)

        if weather_event:
            if weather_event == "rain":
                icon, label, color = "🌧", "RAIN — Open Palm to clear!", (90, 150, 220)
            else:
                icon, label, color = "💨", "WIND — Fist to clear!", (200, 200, 90)

            pygame.draw.rect(self.screen, (20, 20, 28),
                             (20, 220, 360, 60), border_radius=10)
            pygame.draw.rect(self.screen, color,
                             (20, 220, 360, 60), 2, border_radius=10)
            self.draw_text(f"{icon} {label}", self.font_small,
                           color, 32, 232)
            self.draw_text(f"Clears in {weather_time_remaining:.1f}s",
                           self.font_tiny, (180, 180, 180), 32, 262)

    def draw_precision_hud(self, flowers_bloomed, streak, multiplier,
                           wilts, max_wilts, score):
        self.draw_text(f"Score: {score}",
                       self.font_medium, config.GOLD, 20, 130)
        self.draw_text(f"Flowers: {flowers_bloomed}",
                       self.font_small, config.WHITE, 20, 180)
        self.draw_text(f"Streak: {streak}  (x{multiplier})",
                       self.font_small, config.GOLD, 20, 215)

        wilt_color = (200, 50, 50) if wilts >= max_wilts - 1 \
            else (220, 170, 60)
        self.draw_text(f"Wilts: {wilts} / {max_wilts}",
                       self.font_small, wilt_color, 20, 250)

    def draw_random_hud(self, time_left, score, flowers_bloomed,
                        required_gesture, warning_active):
        self.draw_text(f"Time: {int(time_left)}s",
                       self.font_medium, config.WHITE, 20, 130)
        self.draw_text(f"Score: {score}",
                       self.font_small, config.GOLD, 20, 180)
        self.draw_text(f"Flowers: {flowers_bloomed}",
                       self.font_small, config.WHITE, 20, 215)

        name = self.GESTURE_NAMES.get(required_gesture, "")
        self.draw_text_centered(f"Required: {name}",
                                self.font_medium, config.GOLD, 160)

        if warning_active:
            self.draw_text_centered("GESTURE CHANGED!",
                                    self.font_large, (220, 50, 50), 200)

    def draw_cam_feed(self, cam_surface, mirrored=False):
        if cam_surface:
            self.screen.blit(cam_surface,
                             (config.CAM_X, config.CAM_Y))
            pygame.draw.rect(self.screen, config.GOLD,
                             (config.CAM_X - 2, config.CAM_Y - 2,
                              config.CAM_WIDTH + 4,
                              config.CAM_HEIGHT + 4), 2)
            self.draw_text("Your Hand", self.font_tiny,
                           (150, 150, 150),
                           config.CAM_X,
                           config.CAM_Y + config.CAM_HEIGHT + 5)
            if mirrored:
                self.draw_text("MIRRORED", self.font_tiny,
                               config.GOLD,
                               config.CAM_X, config.CAM_Y - 18)

    def draw_stage_label(self, stage):
        stage_names = {
            config.STAGE_SEED:        "Seed",
            config.STAGE_BUD:         "Bud",
            config.STAGE_SMALL_BLOOM: "Small Bloom",
            config.STAGE_TALL_BLOOM:  "Tall Bloom",
            config.STAGE_WIDE_BLOOM:  "Wide Bloom — Complete!",
        }
        name = stage_names.get(stage, "")
        self.draw_text_centered(name, self.font_medium,
                                config.GOLD,
                                config.SCREEN_HEIGHT - 80)

    def draw_game_over(self, level, score, flowers_bloomed,
                       level_complete=False):
        self.screen.fill((10, 10, 15))
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, 0, config.SCREEN_WIDTH, 3))
        pygame.draw.rect(self.screen, config.GOLD,
                         (0, config.SCREEN_HEIGHT - 3,
                          config.SCREEN_WIDTH, 3))

        self.draw_text_centered("GAME OVER",
                                self.font_large, config.WHITE, 120)

        pygame.draw.rect(self.screen, (50, 50, 50),
                         (config.SCREEN_WIDTH // 2 - 300,
                          165, 600, 1))

        if level == 1:
            if level_complete:
                self.draw_text_centered("Collection Complete!",
                                        self.font_medium,
                                        (50, 200, 50), 200)
            else:
                self.draw_text_centered("Time is Up!",
                                        self.font_medium,
                                        config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == 2:
            self.draw_text_centered("Survival Mode — Game Over!",
                                    self.font_medium, config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == "speedrush":
            self.draw_text_centered("Speed Rush — Time's Up!",
                                    self.font_medium, config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == "weather":
            if level_complete:
                self.draw_text_centered("Weather — You Survived!",
                                        self.font_medium,
                                        (50, 200, 50), 200)
            else:
                self.draw_text_centered("Weather — Time's Up!",
                                        self.font_medium,
                                        config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == "precision":
            self.draw_text_centered("Precision — 3 Wilts!",
                                    self.font_medium, config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == "mirror":
            if level_complete:
                self.draw_text_centered("Mirror — Collection Complete!",
                                        self.font_medium,
                                        (50, 200, 50), 200)
            else:
                self.draw_text_centered("Mirror — Time's Up!",
                                        self.font_medium,
                                        config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)
        elif level == "random":
            self.draw_text_centered("Random — Time's Up!",
                                    self.font_medium, config.GOLD, 200)
            self.draw_text_centered(f"Final Score:  {score}",
                                    self.font_small, config.GOLD, 250)
            self.draw_text_centered(
                f"Flowers Bloomed:  {flowers_bloomed}",
                self.font_small, (180, 180, 180), 285)

        pygame.draw.rect(self.screen, (50, 50, 50),
                         (config.SCREEN_WIDTH // 2 - 300,
                          320, 600, 1))

        self.draw_text_centered("LEADERBOARD",
                                self.font_small, config.GOLD, 345)
        if self.leaderboard:
            for i, entry in enumerate(self.leaderboard[:5]):
                self.draw_text_centered(
                    f"{i+1}.   {entry['name']}   —   "
                    f"{entry['score']}   (Level {entry['level']})",
                    self.font_small, (180, 180, 180),
                    385 + i * 38)
        else:
            self.draw_text_centered("No scores yet!",
                                    self.font_small,
                                    (120, 120, 120), 385)

        pygame.draw.rect(self.screen, (50, 50, 50),
                         (config.SCREEN_WIDTH // 2 - 300,
                          585, 600, 1))

        self.draw_text_centered(
            "R — Restart     M — Menu     Q — Quit",
            self.font_tiny, (100, 100, 100), 610)

    def add_to_leaderboard(self, name, score, level):
        self.leaderboard.append({
            "name": name,
            "score": score,
            "level": level
        })
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:10]

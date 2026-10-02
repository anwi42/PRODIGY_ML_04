# main.py

import pygame
import cv2
import sys
import config
from gesture import GestureDetector
from flower import Flower
from game import Game
from ui import UI
from modes import (
    ZenMode,
    SpeedRushMode,
    WeatherMode,
    PrecisionMode,
    MirrorMode,
    RandomMode,
)

def convert_frame_to_surface(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (config.CAM_WIDTH, config.CAM_HEIGHT))
    surface = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))
    return surface

def draw_color_label(screen, color_name):
    color_font = pygame.font.SysFont("Arial", 28, bold=True)
    color_map = {
        "pink":   (255, 105, 180),
        "yellow": (255, 220, 50),
        "white":  (240, 240, 240),
        "red":    (220, 50, 50),
    }
    color = color_map.get(color_name, config.WHITE)
    label = color_font.render(
        color_name.capitalize() + " Flower", True, color)
    label_rect = label.get_rect(
        center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 110))
    screen.blit(label, label_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()

    detector = GestureDetector()
    flower = Flower(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 80)
    game = Game()
    ui = UI(screen)

    # Game states
    STATE_LANDING = "landing"
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    STATE_NAME_INPUT = "name_input"
    STATE_ZEN = "zen"
    STATE_SPEEDRUSH = "speedrush"
    STATE_SPEEDRUSH_GAMEOVER = "speedrush_gameover"
    STATE_WEATHER = "weather"
    STATE_WEATHER_GAMEOVER = "weather_gameover"
    STATE_PRECISION = "precision"
    STATE_PRECISION_GAMEOVER = "precision_gameover"
    STATE_MIRROR = "mirror"
    STATE_MIRROR_GAMEOVER = "mirror_gameover"
    STATE_RANDOM = "random"
    STATE_RANDOM_GAMEOVER = "random_gameover"

    state = STATE_LANDING

    state = STATE_MENU
    cam_surface = None
    confirmed_gesture = config.GESTURE_UNKNOWN
    raw_gesture = config.GESTURE_UNKNOWN
    hold_progress = 0.0
    player_name = ""
    score_saved = False
    survival_started = False
    zen_mode = None
    speedrush_mode = None
    weather_mode = None
    precision_mode = None
    mirror_mode = None
    random_mode = None
    name_input_source = "game"

    def new_flower():
        return Flower(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 80)

    def reset_hold_time():
        detector.hold_time = config.GESTURE_HOLD_TIME

    while True:
        clock.tick(config.FPS)

        # --- Read webcam every frame ---
        frame, confirmed_gesture, raw_gesture, hold_progress = \
            detector.read_frame()
        if frame is not None:
            cam_surface = convert_frame_to_surface(frame)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                detector.release()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Landing state
                if state == STATE_LANDING:
                    if event.key == pygame.K_RETURN:
                        state = STATE_MENU

                # Menu state
                elif state == STATE_MENU:
                    if event.key == pygame.K_1:
                        game.set_level(1)
                        flower = new_flower()
                        state = STATE_PLAYING
                        score_saved = False
                        survival_started = False

                    elif event.key == pygame.K_2:
                        game.set_level(2)
                        flower = new_flower()
                        state = STATE_PLAYING
                        score_saved = False
                        survival_started = False

                    elif event.key == pygame.K_3:
                        zen_mode = ZenMode()
                        flower = new_flower()
                        state = STATE_ZEN
                        score_saved = False

                    elif event.key == pygame.K_4:
                        speedrush_mode = SpeedRushMode(detector)
                        flower = new_flower()
                        state = STATE_SPEEDRUSH
                        score_saved = False

                    elif event.key == pygame.K_5:
                        weather_mode = WeatherMode(detector)
                        flower = new_flower()
                        state = STATE_WEATHER
                        score_saved = False

                    elif event.key == pygame.K_6:
                        precision_mode = PrecisionMode(detector)
                        flower = new_flower()
                        state = STATE_PRECISION
                        score_saved = False

                    elif event.key == pygame.K_7:
                        mirror_mode = MirrorMode()
                        flower = new_flower()
                        state = STATE_MIRROR
                        score_saved = False

                    elif event.key == pygame.K_8:
                        random_mode = RandomMode()
                        flower = new_flower()
                        state = STATE_RANDOM
                        score_saved = False

                # Zen mode state
                elif state == STATE_ZEN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                # Speed Rush state
                elif state == STATE_SPEEDRUSH:
                    if event.key == pygame.K_ESCAPE:
                        reset_hold_time()
                        state = STATE_MENU

                # Weather state
                elif state == STATE_WEATHER:
                    if event.key == pygame.K_ESCAPE:
                        reset_hold_time()
                        state = STATE_MENU

                # Precision state
                elif state == STATE_PRECISION:
                    if event.key == pygame.K_ESCAPE:
                        reset_hold_time()
                        state = STATE_MENU

                # Mirror state
                elif state == STATE_MIRROR:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                # Random state
                elif state == STATE_RANDOM:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                # Speed Rush game over state
                elif state == STATE_SPEEDRUSH_GAMEOVER:
                    if event.key == pygame.K_r:
                        speedrush_mode.reset()
                        flower = new_flower()
                        state = STATE_SPEEDRUSH
                        score_saved = False
                    elif event.key == pygame.K_m:
                        reset_hold_time()
                        state = STATE_MENU
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Weather game over state
                elif state == STATE_WEATHER_GAMEOVER:
                    if event.key == pygame.K_r:
                        weather_mode.reset()
                        flower = new_flower()
                        state = STATE_WEATHER
                        score_saved = False
                    elif event.key == pygame.K_m:
                        reset_hold_time()
                        state = STATE_MENU
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Precision game over state
                elif state == STATE_PRECISION_GAMEOVER:
                    if event.key == pygame.K_r:
                        precision_mode.reset()
                        flower = new_flower()
                        state = STATE_PRECISION
                        score_saved = False
                    elif event.key == pygame.K_m:
                        reset_hold_time()
                        state = STATE_MENU
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Mirror game over state
                elif state == STATE_MIRROR_GAMEOVER:
                    if event.key == pygame.K_r:
                        mirror_mode.reset()
                        flower = new_flower()
                        state = STATE_MIRROR
                        score_saved = False
                    elif event.key == pygame.K_m:
                        state = STATE_MENU
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Random game over state
                elif state == STATE_RANDOM_GAMEOVER:
                    if event.key == pygame.K_r:
                        random_mode.reset()
                        flower = new_flower()
                        state = STATE_RANDOM
                        score_saved = False
                    elif event.key == pygame.K_m:
                        state = STATE_MENU
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Game over state
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        game.reset()
                        if game.level == 1:
                            game.generate_timed_bloom_targets()
                        flower = new_flower()
                        state = STATE_PLAYING
                        score_saved = False
                        survival_started = False
                    elif event.key == pygame.K_m:
                        state = STATE_MENU
                        survival_started = False
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Name input state
                elif state == STATE_NAME_INPUT:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        name = player_name.strip()
                        if name_input_source == "speedrush":
                            ui.add_to_leaderboard(
                                name, speedrush_mode.score, "Speed Rush")
                            state = STATE_SPEEDRUSH_GAMEOVER
                        elif name_input_source == "weather":
                            ui.add_to_leaderboard(
                                name, weather_mode.score, "Weather")
                            state = STATE_WEATHER_GAMEOVER
                        elif name_input_source == "precision":
                            ui.add_to_leaderboard(
                                name, precision_mode.score, "Precision")
                            state = STATE_PRECISION_GAMEOVER
                        elif name_input_source == "mirror":
                            ui.add_to_leaderboard(
                                name, mirror_mode.score, "Mirror")
                            state = STATE_MIRROR_GAMEOVER
                        elif name_input_source == "random":
                            ui.add_to_leaderboard(
                                name, random_mode.score, "Random")
                            state = STATE_RANDOM_GAMEOVER
                        else:
                            ui.add_to_leaderboard(
                                name, game.score, game.level)
                            state = STATE_GAME_OVER
                        score_saved = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15:
                            player_name += event.unicode

        # --- Update game logic ---
        if state == STATE_PLAYING:

            # Spawn first plant for Survival
            if game.level == 2 and not survival_started:
                game.spawn_next_plant(flower)
                survival_started = True

            game.update(confirmed_gesture, flower)
            flower.update()

            if game.game_over and not score_saved:
                player_name = ""
                name_input_source = "game"
                state = STATE_NAME_INPUT

        elif state == STATE_ZEN:
            zen_mode.update(confirmed_gesture, flower)
            flower.update()

        elif state == STATE_SPEEDRUSH:
            speedrush_mode.update(confirmed_gesture, flower)
            flower.update()

            if speedrush_mode.game_over and not score_saved:
                player_name = ""
                name_input_source = "speedrush"
                state = STATE_NAME_INPUT

        elif state == STATE_WEATHER:
            weather_mode.update(confirmed_gesture, flower)
            flower.update()

            if weather_mode.game_over and not score_saved:
                player_name = ""
                name_input_source = "weather"
                state = STATE_NAME_INPUT

        elif state == STATE_PRECISION:
            precision_mode.update(confirmed_gesture, flower)
            flower.update()

            if precision_mode.game_over and not score_saved:
                player_name = ""
                name_input_source = "precision"
                state = STATE_NAME_INPUT

        elif state == STATE_MIRROR:
            mirror_mode.update(confirmed_gesture, flower)
            flower.update()

            if mirror_mode.game_over and not score_saved:
                player_name = ""
                name_input_source = "mirror"
                state = STATE_NAME_INPUT

        elif state == STATE_RANDOM:
            random_mode.update(confirmed_gesture, flower)
            flower.update()

            if random_mode.game_over and not score_saved:
                player_name = ""
                name_input_source = "random"
                state = STATE_NAME_INPUT

        # --- Drawing ---
        if state == STATE_LANDING:
            ui.draw_landing()

        elif state == STATE_MENU:
            ui.draw_menu()

        elif state == STATE_PLAYING:
            ui.draw_background(danger=game.danger_mode)
            flower.draw(screen)

            # Stage label only for flowers not weeds
            if not flower.is_weed:
                ui.draw_stage_label(flower.stage)

            # Gesture prompt or weed warning
            if game.level == 2 and game.waiting_on_weed:
                ui.draw_weed_prompt()
            else:
                ui.draw_gesture_prompt(
                    flower.get_required_gesture(),
                    raw_gesture,
                    hold_progress
                )

            # Show flower color name in Timed Bloom
            if game.level == 1:
                draw_color_label(screen, game.current_color_name)

            ui.draw_cam_feed(cam_surface)

            if game.level == 1:
                ui.draw_level1_hud(
                    game.time_left,
                    game.score,
                    game.targets,
                    game.collection
                )
            elif game.level == 2:
                ui.draw_level2_hud(
                    game.lives,
                    game.score,
                    game.survival_time_left,
                    game.flowers_bloomed,
                    game.stage_time_limit
                )

        elif state == STATE_ZEN:
            ui.draw_background(zen=True)
            flower.draw(screen)

            if not flower.is_weed:
                ui.draw_stage_label(flower.stage)

            ui.draw_gesture_prompt(
                flower.get_required_gesture(),
                raw_gesture,
                hold_progress
            )

            ui.draw_cam_feed(cam_surface)
            ui.draw_zen_hud(zen_mode.flowers_bloomed)

        elif state == STATE_SPEEDRUSH:
            ui.draw_background()
            flower.draw(screen)

            if not flower.is_weed:
                ui.draw_stage_label(flower.stage)

            ui.draw_gesture_prompt(
                flower.get_required_gesture(),
                raw_gesture,
                hold_progress
            )

            ui.draw_cam_feed(cam_surface)
            ui.draw_speedrush_hud(
                speedrush_mode.time_left,
                speedrush_mode.speed_multiplier,
                speedrush_mode.flowers_bloomed
            )

        elif state == STATE_WEATHER:
            ui.draw_background()

            ox, oy = weather_mode.shake_offset
            flower.x += ox
            flower.y += oy
            flower.draw(screen)
            flower.x -= ox
            flower.y -= oy

            ui.draw_stage_label(flower.stage)

            ui.draw_gesture_prompt(
                flower.get_required_gesture(),
                raw_gesture,
                hold_progress
            )

            ui.draw_cam_feed(cam_surface)
            ui.draw_weather_hud(
                weather_mode.time_left,
                weather_mode.flowers_bloomed,
                weather_mode.weather_event,
                weather_mode.weather_time_remaining
            )

        elif state == STATE_PRECISION:
            ui.draw_background()
            flower.draw(screen)

            ui.draw_stage_label(flower.stage)

            ui.draw_gesture_prompt(
                flower.get_required_gesture(),
                raw_gesture,
                hold_progress
            )

            ui.draw_cam_feed(cam_surface)
            ui.draw_precision_hud(
                precision_mode.flowers_bloomed,
                precision_mode.streak,
                precision_mode.get_multiplier(),
                precision_mode.wilts,
                config.PRECISION_MAX_WILTS,
                precision_mode.score
            )

        elif state == STATE_MIRROR:
            ui.draw_background()
            flower.draw(screen)

            if not flower.is_weed:
                ui.draw_stage_label(flower.stage)

            ui.draw_gesture_prompt(
                flower.get_required_gesture(),
                raw_gesture,
                hold_progress
            )

            draw_color_label(screen, mirror_mode.current_color_name)

            mirrored_surface = None
            if cam_surface is not None:
                mirrored_surface = pygame.transform.flip(
                    cam_surface, True, False)
            ui.draw_cam_feed(mirrored_surface, mirrored=True)

            ui.draw_level1_hud(
                mirror_mode.time_left,
                mirror_mode.score,
                mirror_mode.targets,
                mirror_mode.collection
            )

        elif state == STATE_RANDOM:
            ui.draw_background()
            flower.draw(screen)

            ui.draw_stage_label(flower.stage)

            required = random_mode.get_required_gesture(flower)
            ui.draw_gesture_prompt(required, raw_gesture, hold_progress)

            ui.draw_cam_feed(cam_surface)
            ui.draw_random_hud(
                random_mode.time_left,
                random_mode.score,
                random_mode.flowers_bloomed,
                required,
                random_mode.is_warning_active()
            )

        elif state == STATE_NAME_INPUT:
            ui.draw_background()
            font_large = pygame.font.SysFont("Arial", config.FONT_LARGE,
                                             bold=True)
            font_medium = pygame.font.SysFont("Arial", config.FONT_MEDIUM)
            font_small = pygame.font.SysFont("Arial", config.FONT_SMALL)

            # Title
            text = font_large.render("GAME OVER", True, config.WHITE)
            rect = text.get_rect(
                center=(config.SCREEN_WIDTH // 2, 200))
            screen.blit(text, rect)

            # Prompt
            text2 = font_medium.render(
                "Enter your name for the leaderboard:",
                True, (180, 180, 180))
            rect2 = text2.get_rect(
                center=(config.SCREEN_WIDTH // 2, 310))
            screen.blit(text2, rect2)

            # Name box
            pygame.draw.rect(screen, (20, 20, 28),
                             (config.SCREEN_WIDTH // 2 - 220,
                              360, 440, 55),
                             border_radius=8)
            pygame.draw.rect(screen, config.GOLD,
                             (config.SCREEN_WIDTH // 2 - 220,
                              360, 440, 55),
                             2, border_radius=8)
            name_text = font_medium.render(player_name, True, config.WHITE)
            name_rect = name_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, 387))
            screen.blit(name_text, name_rect)

            # Instruction
            text3 = font_small.render(
                "Press Enter to confirm",
                True, (120, 120, 120))
            rect3 = text3.get_rect(
                center=(config.SCREEN_WIDTH // 2, 440))
            screen.blit(text3, rect3)

        elif state == STATE_SPEEDRUSH_GAMEOVER:
            ui.draw_game_over(
                "speedrush",
                speedrush_mode.score,
                speedrush_mode.flowers_bloomed
            )

        elif state == STATE_WEATHER_GAMEOVER:
            ui.draw_game_over(
                "weather",
                weather_mode.score,
                weather_mode.flowers_bloomed,
                weather_mode.win
            )

        elif state == STATE_PRECISION_GAMEOVER:
            ui.draw_game_over(
                "precision",
                precision_mode.score,
                precision_mode.flowers_bloomed
            )

        elif state == STATE_MIRROR_GAMEOVER:
            ui.draw_game_over(
                "mirror",
                mirror_mode.score,
                mirror_mode.flowers_bloomed,
                mirror_mode.level_complete
            )

        elif state == STATE_RANDOM_GAMEOVER:
            ui.draw_game_over(
                "random",
                random_mode.score,
                random_mode.flowers_bloomed
            )

        elif state == STATE_GAME_OVER:
            ui.draw_game_over(
                game.level,
                game.score,
                game.flowers_bloomed,
                game.level_complete
            )

        pygame.display.flip()

    detector.release()
    pygame.quit()

if __name__ == "__main__":
    main()

# main.py

import pygame
import cv2
import sys
import config
from gesture import GestureDetector
from flower import Flower
from game import Game
from ui import UI

def convert_frame_to_surface(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (config.CAM_WIDTH, config.CAM_HEIGHT))
    surface = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))
    return surface

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

    state = STATE_LANDING

    state = STATE_MENU
    cam_surface = None
    confirmed_gesture = config.GESTURE_UNKNOWN
    raw_gesture = config.GESTURE_UNKNOWN
    hold_progress = 0.0
    player_name = ""
    score_saved = False
    level3_started = False

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
                        flower = Flower(config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT - 80)
                        state = STATE_PLAYING
                        score_saved = False
                        level3_started = False

                    elif event.key == pygame.K_2:
                        game.set_level(2)
                        flower = Flower(config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT - 80)
                        state = STATE_PLAYING
                        score_saved = False
                        level3_started = False

                    elif event.key == pygame.K_3:
                        game.set_level(3)
                        flower = Flower(config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT - 80)
                        state = STATE_PLAYING
                        score_saved = False
                        level3_started = False

                # Game over state
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        game.reset()
                        if game.level == 2:
                            game.generate_level2_targets()
                        flower = Flower(config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT - 80)
                        state = STATE_PLAYING
                        score_saved = False
                        level3_started = False
                    elif event.key == pygame.K_m:
                        state = STATE_MENU
                        level3_started = False
                    elif event.key == pygame.K_q:
                        detector.release()
                        pygame.quit()
                        sys.exit()

                # Name input state
                elif state == STATE_NAME_INPUT:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        ui.add_to_leaderboard(
                            player_name.strip(),
                            game.score,
                            game.level
                        )
                        score_saved = True
                        state = STATE_GAME_OVER
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15:
                            player_name += event.unicode

        # --- Update game logic ---
        if state == STATE_PLAYING:

            # Spawn first plant for level 3
            if game.level == 3 and not level3_started:
                game.spawn_next_plant(flower)
                level3_started = True

            game.update(confirmed_gesture, flower)
            flower.update()

            if game.game_over and not score_saved:
                player_name = ""
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
            if game.level == 3 and game.waiting_on_weed:
                ui.draw_weed_prompt()
            else:
                ui.draw_gesture_prompt(
                    flower.get_required_gesture(),
                    raw_gesture,
                    hold_progress
                )

            # Show flower color name in level 2
            if game.level == 2:
                color_font = pygame.font.SysFont("Arial", 28, bold=True)
                color_map = {
                    "pink":   (255, 105, 180),
                    "yellow": (255, 220, 50),
                    "white":  (240, 240, 240),
                    "red":    (220, 50, 50),
                }
                color = color_map.get(
                    game.current_color_name, config.WHITE)
                label = color_font.render(
                    game.current_color_name.capitalize() + " Flower",
                    True, color)
                label_rect = label.get_rect(
                    center=(config.SCREEN_WIDTH // 2,
                            config.SCREEN_HEIGHT - 110))
                screen.blit(label, label_rect)

            ui.draw_cam_feed(cam_surface)

            if game.level == 1:
                ui.draw_level1_hud(game.flowers_bloomed, game.streak)
            elif game.level == 2:
                ui.draw_level2_hud(
                    game.time_left,
                    game.score,
                    game.targets,
                    game.collection
                )
            elif game.level == 3:
                ui.draw_level3_hud(
                    game.lives,
                    game.score,
                    game.level3_time_left,
                    game.flowers_bloomed,
                    game.stage_time_limit
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
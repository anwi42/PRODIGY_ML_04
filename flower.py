# flower.py

import pygame
import math
import random
import config

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -1)
        self.life = 1.0
        self.radius = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 0.03

    def draw(self, screen):
        if self.life > 0:
            color = (
                min(255, self.color[0]),
                min(255, self.color[1]),
                min(255, self.color[2])
            )
            pygame.draw.circle(screen, color,
                               (int(self.x), int(self.y)), self.radius)


class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stage = config.STAGE_SEED
        self.color_index = 0
        self.color = config.FLOWER_COLORS[self.color_index]
        self.particles = []
        self.glow = 0
        self.glow_direction = 1
        self.is_golden = False
        self.is_weed = False

    def set_golden(self):
        self.is_golden = True
        self.color = (255, 215, 0)

    def set_weed(self):
        self.is_weed = True

    def get_required_gesture(self):
        if self.is_weed:
            return None
        if self.stage == config.STAGE_SEED:
            return config.GESTURE_OPEN_PALM
        elif self.stage == config.STAGE_BUD:
            return config.GESTURE_PEACE
        elif self.stage == config.STAGE_SMALL_BLOOM:
            return config.GESTURE_FIST
        elif self.stage == config.STAGE_TALL_BLOOM:
            return config.GESTURE_POINT_UP
        return None

    def advance_stage(self):
        if self.stage < config.STAGE_WIDE_BLOOM:
            self.stage += 1
            self.spawn_particles()
            return True
        return False

    def is_complete(self):
        return self.stage == config.STAGE_WIDE_BLOOM

    def reset(self, cycle_color=False):
        self.stage = config.STAGE_SEED
        self.is_golden = False
        self.is_weed = False
        if cycle_color:
            self.color_index = (self.color_index + 1) % len(config.FLOWER_COLORS)
            self.color = config.FLOWER_COLORS[self.color_index]
        else:
            self.color = config.FLOWER_COLORS[self.color_index]
        self.particles = []
        self.glow = 0

    def spawn_particles(self):
        color = (255, 215, 0) if self.is_golden else self.color
        for _ in range(30):
            self.particles.append(
                Particle(self.x, self.y - 150, color))
        for _ in range(15):
            self.particles.append(
                Particle(self.x, self.y - 150, config.GOLD))

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()
        self.glow += 3 * self.glow_direction
        if self.glow >= 80 or self.glow <= 0:
            self.glow_direction *= -1

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

        if self.is_weed:
            self.draw_weed(screen)
            return

        if self.stage == config.STAGE_SEED:
            self.draw_seed(screen)
        elif self.stage == config.STAGE_BUD:
            self.draw_bud(screen)
        elif self.stage == config.STAGE_SMALL_BLOOM:
            self.draw_small_bloom(screen)
        elif self.stage == config.STAGE_TALL_BLOOM:
            self.draw_tall_bloom(screen)
        elif self.stage == config.STAGE_WIDE_BLOOM:
            self.draw_wide_bloom(screen)

    def draw_stem(self, screen, height):
        color = (180, 160, 0) if self.is_golden else (34, 120, 34)
        pygame.draw.line(screen, color,
                         (self.x, self.y),
                         (self.x, self.y - height), 5)

    def draw_seed(self, screen):
        color = (200, 170, 0) if self.is_golden else (139, 90, 43)
        pygame.draw.ellipse(screen, color,
                            (self.x - 12, self.y - 20, 24, 20))

    def draw_bud(self, screen):
        self.draw_stem(screen, 80)
        pygame.draw.ellipse(screen, (34, 120, 34),
                            (self.x - 14, self.y - 110, 28, 36))
        pygame.draw.ellipse(screen, self.color,
                            (self.x - 10, self.y - 108, 20, 28))

    def draw_small_bloom(self, screen):
        self.draw_stem(screen, 120)
        cx = self.x
        cy = self.y - 130
        for i in range(6):
            angle = math.radians(i * 60)
            px = cx + int(math.cos(angle) * 35)
            py = cy + int(math.sin(angle) * 35)
            pygame.draw.ellipse(screen, self.color,
                                (px - 18, py - 18, 36, 36))
        pygame.draw.circle(screen, config.GOLD, (cx, cy), 18)
        pygame.draw.circle(screen, (255, 240, 100), (cx, cy), 10)

        # Golden sparkle ring
        if self.is_golden:
            for i in range(8):
                angle = math.radians(i * 45 + self.glow)
                sx = cx + int(math.cos(angle) * 60)
                sy = cy + int(math.sin(angle) * 60)
                pygame.draw.circle(screen, config.GOLD, (sx, sy), 4)

    def draw_tall_bloom(self, screen):
        self.draw_stem(screen, 200)
        cx = self.x
        cy = self.y - 210
        pygame.draw.ellipse(screen, (34, 120, 34),
                            (self.x - 35, self.y - 130, 35, 18))
        pygame.draw.ellipse(screen, (34, 120, 34),
                            (self.x, self.y - 160, 35, 18))
        glow_color = (
            max(0, min(255, self.color[0] + self.glow // 2)),
            max(0, min(255, self.color[1] + self.glow // 2)),
            max(0, min(255, self.color[2] + self.glow // 2))
        )
        
        for i in range(6):
            angle = math.radians(i * 60)
            px = cx + int(math.cos(angle) * 38)
            py = cy + int(math.sin(angle) * 38)
            pygame.draw.ellipse(screen, glow_color,
                                (px - 20, py - 20, 40, 40))
        pygame.draw.circle(screen, config.GOLD, (cx, cy), 20)
        pygame.draw.circle(screen, (255, 240, 100), (cx, cy), 12)

        if self.is_golden:
            for i in range(8):
                angle = math.radians(i * 45 + self.glow)
                sx = cx + int(math.cos(angle) * 70)
                sy = cy + int(math.sin(angle) * 70)
                pygame.draw.circle(screen, config.GOLD, (sx, sy), 4)

    def draw_wide_bloom(self, screen):
        self.draw_stem(screen, 200)
        cx = self.x
        cy = self.y - 210
        pygame.draw.ellipse(screen, (34, 120, 34),
                            (self.x - 35, self.y - 130, 35, 18))
        pygame.draw.ellipse(screen, (34, 120, 34),
                            (self.x, self.y - 160, 35, 18))
        glow_color = (
            max(0, min(255, self.color[0] + self.glow)),
            max(0, min(255, self.color[1] + self.glow // 2)),
            max(0, min(255, self.color[2] + self.glow))
        )
        
        for i in range(10):
            angle = math.radians(i * 36)
            px = cx + int(math.cos(angle) * 55)
            py = cy + int(math.sin(angle) * 55)
            pygame.draw.ellipse(screen, glow_color,
                                (px - 26, py - 26, 52, 52))
        for i in range(10):
            angle = math.radians(i * 36 + 18)
            px = cx + int(math.cos(angle) * 35)
            py = cy + int(math.sin(angle) * 35)
            pygame.draw.ellipse(screen, self.color,
                                (px - 16, py - 16, 32, 32))
        pygame.draw.circle(screen, config.GOLD, (cx, cy), 24)
        pygame.draw.circle(screen, (255, 240, 100), (cx, cy), 14)
        for i in range(8):
            angle = math.radians(i * 45 + self.glow)
            sx = cx + int(math.cos(angle) * 85)
            sy = cy + int(math.sin(angle) * 85)
            pygame.draw.circle(screen, config.GOLD, (sx, sy), 4)

    def draw_weed(self, screen):
        # Stem
        pygame.draw.line(screen, (60, 100, 20),
                         (self.x, self.y),
                         (self.x, self.y - 100), 5)
        # Leaves
        pygame.draw.ellipse(screen, (60, 100, 20),
                            (self.x - 40, self.y - 80, 40, 16))
        pygame.draw.ellipse(screen, (60, 100, 20),
                            (self.x, self.y - 60, 40, 16))
        pygame.draw.ellipse(screen, (60, 100, 20),
                            (self.x - 35, self.y - 40, 35, 16))
        # Jagged top
        pygame.draw.polygon(screen, (80, 120, 20), [
            (self.x, self.y - 100),
            (self.x - 15, self.y - 120),
            (self.x - 5, self.y - 110),
            (self.x, self.y - 130),
            (self.x + 5, self.y - 110),
            (self.x + 15, self.y - 120),
        ])
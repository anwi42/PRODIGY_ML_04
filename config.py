# config.py

# --- Screen Settings ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30
TITLE = "Petal Rush"

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
DARK_RED = (120, 20, 20)
GREEN = (34, 85, 34)
DARK_GREEN = (15, 40, 15)
GOLD = (255, 215, 0)
GREY = (180, 180, 180)
LIGHT_GREY = (220, 220, 220)
PURPLE = (120, 50, 180)
CYAN = (50, 200, 200)

# --- Flower Colors (Level 1 cycles through these) ---
FLOWER_COLORS = [
    (255, 105, 180),  # Pink
    (220, 50, 50),    # Red
    (255, 255, 255),  # White
    (255, 220, 50),   # Yellow
    (180, 100, 255),  # Purple
]

# --- Gesture Labels ---
GESTURE_OPEN_PALM = "open_palm"
GESTURE_PEACE = "peace_sign"
GESTURE_FIST = "fist"
GESTURE_POINT_UP = "point_up"
GESTURE_UNKNOWN = "unknown"

# --- Flower Stages ---
STAGE_SEED = 0
STAGE_BUD = 1
STAGE_SMALL_BLOOM = 2
STAGE_TALL_BLOOM = 3
STAGE_WIDE_BLOOM = 4


# --- Level 1 Settings ---
LEVEL1_FLOWER_TARGET = 5

# --- Level 2 Settings ---
LEVEL2_TIME_LIMIT = 60
LEVEL2_BONUS_PER_SECOND = 5

# Flower colors for Level 2
LEVEL2_FLOWER_COLORS = {
    "pink":   (255, 105, 180),
    "yellow": (255, 220, 50),
    "white":  (240, 240, 240),
    "red":    (220, 50, 50),
}

# Spawning probabilities
LEVEL2_NEEDED_CHANCE_EARLY = 0.4   # first 40 seconds
LEVEL2_NEEDED_CHANCE_LATE  = 0.65  # last 20 seconds
LEVEL2_LATE_THRESHOLD = 20         # seconds remaining

# --- Level 3 Settings ---
LEVEL3_LIVES = 3
LEVEL3_TIME_LIMIT = 90
LEVEL3_POINTS_PER_FLOWER = 10
LEVEL3_GOLDEN_POINTS = 30
LEVEL3_WEED_CHANCE = 0.2      # 20% chance a weed appears
LEVEL3_GOLDEN_CHANCE = 0.15   # 15% chance a golden flower appears

# Response time per stage based on time remaining
LEVEL3_EASY_RESPONSE = 4.0    # first 30 seconds
LEVEL3_MEDIUM_RESPONSE = 3.0  # next 30 seconds
LEVEL3_HARD_RESPONSE = 2.0    # last 30 seconds

# --- Webcam Feed Size ---
CAM_WIDTH = 240
CAM_HEIGHT = 180
CAM_X = SCREEN_WIDTH - CAM_WIDTH - 20
CAM_Y = 20

# --- Font Sizes ---
FONT_LARGE = 56
FONT_MEDIUM = 36
FONT_SMALL = 24
FONT_TINY = 18

# --- Gesture Hold Timer ---
GESTURE_HOLD_TIME = 1.0
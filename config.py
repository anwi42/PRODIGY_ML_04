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

# --- Flower Colors (cycled through on reset) ---
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


# --- Timed Bloom Settings ---
TIMED_BLOOM_TIME_LIMIT = 60
TIMED_BLOOM_BONUS_PER_SECOND = 5

# Flower colors for Timed Bloom
TIMED_BLOOM_FLOWER_COLORS = {
    "pink":   (255, 105, 180),
    "yellow": (255, 220, 50),
    "white":  (240, 240, 240),
    "red":    (220, 50, 50),
}

# Spawning probabilities
TIMED_BLOOM_NEEDED_CHANCE_EARLY = 0.4   # first 40 seconds
TIMED_BLOOM_NEEDED_CHANCE_LATE  = 0.65  # last 20 seconds
TIMED_BLOOM_LATE_THRESHOLD = 20         # seconds remaining

# --- Survival Settings ---
SURVIVAL_LIVES = 3
SURVIVAL_TIME_LIMIT = 90
SURVIVAL_POINTS_PER_FLOWER = 10
SURVIVAL_GOLDEN_POINTS = 30
SURVIVAL_WEED_CHANCE = 0.2      # 20% chance a weed appears
SURVIVAL_GOLDEN_CHANCE = 0.15   # 15% chance a golden flower appears

# Response time per stage based on time remaining
SURVIVAL_EASY_RESPONSE = 4.0    # first 30 seconds
SURVIVAL_MEDIUM_RESPONSE = 3.0  # next 30 seconds
SURVIVAL_HARD_RESPONSE = 2.0    # last 30 seconds

# --- Zen Mode Settings ---
ZEN_BG_COLOR = (8, 22, 12)

# --- Speed Rush Settings ---
SPEEDRUSH_TIME_LIMIT = 60
SPEEDRUSH_START_HOLD_TIME = 2.0
SPEEDRUSH_HOLD_DECREASE = 0.2
SPEEDRUSH_SPEEDUP_INTERVAL = 10
SPEEDRUSH_MIN_HOLD_TIME = 0.5
SPEEDRUSH_MISS_PENALTY = 5

# --- Weather Mode Settings ---
WEATHER_TIME_LIMIT = 90
WEATHER_FLOWER_TARGET = 5
WEATHER_POINTS_PER_FLOWER = 10
WEATHER_EVENT_INTERVAL = 20     # seconds between weather events
WEATHER_EVENT_DURATION = 8      # seconds an event lasts if not cleared
WEATHER_RAIN_SLOWDOWN = 0.5     # hold timer slows by +50%
WEATHER_WIND_SHRINK = 0.5       # gesture window shrinks to 50%
WEATHER_SHAKE_PIXELS = 6        # max flower jitter during wind

# --- Precision Mode Settings ---
PRECISION_GESTURE_WINDOW = 0.5
PRECISION_MAX_WILTS = 3
PRECISION_STREAK_TIER1 = 5
PRECISION_MULTIPLIER_TIER1 = 2
PRECISION_STREAK_TIER2 = 10
PRECISION_MULTIPLIER_TIER2 = 3

# --- Random Mode Settings ---
RANDOM_TIME_LIMIT = 90
RANDOM_CHANGE_CHANCE = 0.3       # chance the required gesture changes
RANDOM_WARNING_TIME = 1.0        # warning shown before the change lands
RANDOM_ADAPT_WINDOW = 1.0        # window to earn the adapt bonus
RANDOM_ADAPT_BONUS = 50
RANDOM_POINTS_PER_FLOWER = 10

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
GESTURE_HOLD_TIME = 0.6

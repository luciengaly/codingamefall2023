from vector import Vector


COLORS = ["pink", "yellow", "green", "blue"]

WIDTH = 10000
HEIGHT = 10000

DRONES_PER_PLAYER = 1
NUMBER_OF_PLAYER = 2

UGLY_UPPER_Y_LIMIT = 2500
DRONE_UPPER_Y_LIMIT = 0
DRONE_START_Y = 500

COLORS_PER_FISH = 4
DRONE_MAX_BATTERY = 30
LIGHT_BATTERY_COST = 5
DRONE_BATTERY_REGEN = 1
DRONE_MAX_SCANS = float("inf")

DARK_SCAN_RANGE = 800
LIGHT_SCAN_RANGE = 2000
UGLY_EAT_RANGE = 300
DRONE_HIT_RANGE = 200
FISH_HEARING_RANGE = (DARK_SCAN_RANGE + LIGHT_SCAN_RANGE) // 2

DRONE_MOVE_SPEED = 600
DRONE_SINK_SPEED = 300
DRONE_EMERGENCY_SPEED = 300
DRONE_MOVE_SPEED_LOSS_PER_SCAN = 0

FISH_SWIM_SPEED = 200
FISH_AVOID_RANGE = 600
FISH_FLEE_SPEED = 400
UGLY_ATTACK_SPEED = int(DRONE_MOVE_SPEED * 0.9)
UGLY_SEARCH_SPEED = int(UGLY_ATTACK_SPEED / 2)

FISH_X_SPAWN_LIMIT = 1000
FISH_SPAWN_MIN_SEP = 1000
ALLOW_EMOJI = True

CENTER = Vector((WIDTH - 1) / 2.0, (HEIGHT - 1) / 2.0)
MAX_TURNS = 200
ENABLE_UGLIES = False
FISH_WILL_FLEE = False
FISH_WILL_MOVE = True
SIMPLE_SCANS = True

NUM_DIRECTIONS_ACT = 12

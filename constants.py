# game vars
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 150
COLS = 150
SCROLL_THRESH = 200
RANGE = 5
ATTACK_RANGE = 60
# game fps
FPS = 60

# speed
CHARACTER_SPEED = 30
ARROW_SPEED = 10
FIREBALL_SPEED = 4
ENEMY_SPEED  = 4

# Scale
SCALE = 3
BUTTON_SCALE = 0.5
SAVE_BUTTON_SCALE = 0.5
LOAD_BUTTON_SCALE = 0.5
LEADERBOARD_BUTTON_SCALE = 0.5
CHARACTER_SCALE = 3
BOW_SCALE = 1.5
ITEM_SCALE = 3
ITEM_COLLECT_SCALE = 1
POTION_SCALE = 2
FIREBALL_SCALE = 1

# Tile 
TILE_SIZE = 16 * SCALE
TILE_TYPES = {
    1: 86,
    2: 86,
    3: 86
}

LEVEL_ASSETS = {
    1: "newassets/level1/",
    2: "newassets/level2/",
    3: "newassets/level3/"
}

LEVEL_CHARACTERS = {
    1: ['elf', 'turkey'],
    2: ['elf', 'turkey'],
    3: ['elf', 'turkey']
}

LEVEL_ITEMS = {
    1: ['chest', 'meat'],
    2: ['chest', 'meat'],
    3: ['chest', 'meat']
}

ENEMY_TILE_MAP = {
    1: {
    'turkey': 83,
    },
    2: {
    'turkey': 83,
    },
    3: {
    'turkey': 83,
    }
}

EXIT_TILE_MAP = {
    1: [74],
    2: [74],
    3: [74]
}

BASE_TILES = {
    1: 23,
    2: 23,
    3: 23
}

# Find all obstacle tiles for each level and store in a list
OBSTACLE_TILES_MAP = {
    1: [2,3,4,6,10,13,14,16,27,28,29,32,34,35,36,37,39,40,41,42,43,44,48,49,50,52,55,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,76,77,80],
    2: [2,3,4,6,10,13,14,16,27,28,29,32,34,35,36,37,39,40,41,42,43,44,48,49,50,52,55,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,76,77,80],
    3: [2,3,4,6,10,13,14,16,27,28,29,32,34,35,36,37,39,40,41,42,43,44,48,49,50,52,55,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,76,77,80]
}

REWARD_MAP = {
    'enemy': 100,
    'coin': 10
}

ANIMATION_TYPES = ['idle', 'run']
# cooldowns
SHOT_COOLDOWN = 300

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (0, 0, 0)
MENU_BGCOLOR = (130, 0, 0)
PANEL = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
# sprite offset
CHARACTER_OFFSET = 12
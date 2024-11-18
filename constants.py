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
CHARACTER_SPEED = 5
ARROW_SPEED = 10
FIREBALL_SPEED = 4
ENEMY_SPEED  = 4

# Scale
SCALE = 3
BUTTON_SCALE = 1
CHARACTER_SCALE = 3
BOW_SCALE = 1.5
ITEM_SCALE = 3
POTION_SCALE = 2
FIREBALL_SCALE = 1

# Tile 
TILE_SIZE = 16 * SCALE
TILE_TYPES = {
    1: 85,
    2: 63,
    3: 81
}

LEVEL_ASSETS = {
    1: "newassets/level1/",
    2: "newassets/level2/",
    3: "newassets/level3/"
}

LEVEL_CHARACTERS = {
    1: ['elf', 'turkey'],
    2: ['elf', 'dracula', 'bat', 'ghost'],
    3: ['elf', 'snowman']
}

LEVEL_ITEMS = {
    1: ['chest', 'meat'],
    2: ['chest'],
    3: ['chest']
}

ENEMY_TILE_MAP = {
    1: {
    'turkey': 83,
    },
    2: {
    'dracula': 3,
    'bat': 4,
    'ghost': 5,
    },
    3: {
    'snowman': 6
    }
}

ANIMATION_TYPES = ['idle', 'run']
# cooldowns
SHOT_COOLDOWN = 300

# colors
RED = (255, 0, 0)
BGCOLOR = (0, 0, 0)
MENU_BGCOLOR = (130, 0, 0)
PANEL = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
# sprite offset
CHARACTER_OFFSET = 12
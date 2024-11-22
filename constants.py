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
CHARACTER_SPEED = 10
FLARE_SPEED = 20
ENEMY_SPEED  = 5

# Scale
SCALE = 3
BUTTON_SCALE = 0.5
SAVE_BUTTON_SCALE = 0.5
LOAD_BUTTON_SCALE = 0.5
LEADERBOARD_BUTTON_SCALE = 0.5
CHARACTER_SCALE = 3
GUN_SCALE = 1.5
ITEM_SCALE = 3
ITEM_COLLECT_SCALE = 1
POTION_SCALE = 2
FIREBALL_SCALE = 1

# Tile 
TILE_SIZE = 16 * SCALE
TILE_TYPES = {
    1: 86,
    2: 74,
    3: 63
}

LEVEL_STORY = {
    1: "You are an elf warrior who must reach home and defeat evil turkeys to save your village. There were some previous warriors who failed to do so. But they could defeat a few turkeys and cook them for dinner. If you are lucky, you might find some of cooked turkeys and also find treasure chests.",
    2: "Now you are going to save your friend's village occupied by ghosts of dead turkeys. Defeat the ghosts and reach your friend's home. Ghosts will spook you and suck your blood, so you must collect blood viels to recover your lost blood. In the mean time, you can collect pumpkins to bring it to villagers.",
    3: "WINTER IS COMING!! You must find your way home while collecting gifts left by Santa to take back to your village. Snowmen are guarding the way home. You must defeat them to reach home."
}

LEVEL_ASSETS = {
    1: "assets/level1/",
    2: "assets/level2/",
    3: "assets/level3/"
}

LEVEL_CHARACTERS = {
    1: ['elf', 'turkey'],
    2: ['elf', 'ghost'],
    3: ['elf', 'snowman']
}

LEVEL_ITEMS = {
    1: ['chest', 'meat'],
    2: ['pumpkin', 'blood'],
    3: ['gift', 'ring']
}

AUDIO = {
    'background': 'audio/music.mp3',
    'enemy_killed': 'audio/enemy_killed.mp3',
    'item_collected': 'audio/item_collected.mp3'
}

ENEMY_TILE_MAP = {
    1: {
    'turkey': 83,
    },
    2: {
    'ghost': 0,
    },
    3: {
    'snowman': 27,
    }
}

EXIT_TILE_MAP = {
    1: [74],
    2: [68],
    3: [47]
}

BASE_TILES = {
    1: 23,
    2: 30,
    3: 28
}

# Find all obstacle tiles for each level and store in a list
OBSTACLE_TILES_MAP = {
    1: [2,3,4,6,10,13,14,16,27,28,29,32,34,35,36,37,39,40,41,42,43,44,48,49,50,52,55,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,76,77,80],
    2: [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,31,32,34,37,39,40,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,70,71,],
    3: [0,9,24,35,36,37,38,39,40,41,42,43,44,45,49,50,51,52,53,54,55,56,57,58,59,60,61]
}

REWARDS_TILES_MAP = {
    1: 82,
    2: 1,
    3: 19
}

POTIONS_TILES_MAP = {
    1: 84,
    2: 72,
    3: 33
}

CHARACTER_TILE_MAP = {
    1: 85,
    2: 73,
    3: 62
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
SKY_BLUE = (135, 206, 235)
MENU_BGCOLOR = (0, 0, 0)
PANEL = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
# sprite offset
CHARACTER_OFFSET = 12
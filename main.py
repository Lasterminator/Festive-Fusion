import pygame
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from items import ItemFactory
from world import World
from button import Button
from scoreboard import Scoreboard
from state import GameCaretaker, GameMemento
import json
mixer.init()
# initialize pygame
pygame.init() 

# create a screen with a width and height and set the caption
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Festive Fusion")

# Clock controlling the speed of the game
clock = pygame.time.Clock()

# define game variables
level = 1
current_asset_path = constants.LEVEL_ASSETS[level]
start_game = False
pause_game = False
start_intro = False
show_controls = False
screen_scroll = [0, 0]
player_score = 0
previous_player_score = 0

# define character movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

total_score = 0
show_scoreboard = False
show_input = False
show_leaderboard = False
show_level_intro = False
show_level_select = False
scoreboard = Scoreboard()

#instance of game state
game_caretaker = GameCaretaker()

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# helper function to scale the character image
def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

try:
    pygame.mixer.music.load('assets/level1/audio/music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    print("Error loading background music")

shot_fx = pygame.mixer.Sound('assets/audio/flare_shot.mp3')
shot_fx.set_volume(0.05)
hit_fx = pygame.mixer.Sound('assets/level1/audio/enemy_killed.mp3')
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound('assets/audio/heal.wav')
heal_fx.set_volume(0.5)


def load_audio(level):
    try:
        pygame.mixer.music.load(f'assets/level{level}/audio/music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        shot_fx = pygame.mixer.Sound(f'assets/level{level}/audio/flare_shot.mp3')
        shot_fx.set_volume(0.05)
        hit_fx = pygame.mixer.Sound(f'assets/level{level}/audio/enemy_killed.mp3')
        hit_fx.set_volume(0.5)
        coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
        coin_fx.set_volume(0.5)
        heal_fx = pygame.mixer.Sound('assets/audio/heal.wav')
        heal_fx.set_volume(0.5)

    except:
        print(f"Error loading background music for level {level}")
load_audio(level)
    

# load button images
logo_img = scale_image(pygame.image.load('assets/images/logo.png').convert_alpha(), constants.LOGO_SCALE)
start_img = scale_image(pygame.image.load('assets/images/buttons/button_start.png').convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_image(pygame.image.load('assets/images/buttons/button_restart.png').convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_image(pygame.image.load('assets/images/buttons/button_exit.png').convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_image(pygame.image.load('assets/images/buttons/button_resume.png').convert_alpha(), constants.BUTTON_SCALE)
save_img = scale_image(pygame.image.load('assets/images/buttons/button_save.png').convert_alpha(), constants.SAVE_BUTTON_SCALE)
load_img = scale_image(pygame.image.load('assets/images/buttons/button_load.png').convert_alpha(), constants.LOAD_BUTTON_SCALE)
leaderboard_img = scale_image(pygame.image.load('assets/images/buttons/button_leaderboard.png').convert_alpha(), constants.LEADERBOARD_BUTTON_SCALE)
back_img = scale_image(pygame.image.load('assets/images/buttons/button_back.png').convert_alpha(), constants.BUTTON_SCALE)
level1_img = scale_image(pygame.image.load('assets/images/buttons/button_level1.png').convert_alpha(), constants.LEVEL_BUTTON_SCALE)
level2_img = scale_image(pygame.image.load('assets/images/buttons/button_level2.png').convert_alpha(), constants.LEVEL_BUTTON_SCALE)
level3_img = scale_image(pygame.image.load('assets/images/buttons/button_level3.png').convert_alpha(), constants.LEVEL_BUTTON_SCALE)

# load heart image
heart_empty = scale_image(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_image(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_image(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)

# load coin image
coin_image = []
img = pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
img = scale_image(img, constants.ITEM_SCALE)
coin_image.append(img)

coin_collect_image = []
def load_coin_collect_image(level):
    img = pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
    img = scale_image(img, constants.ITEM_COLLECT_SCALE)
    coin_collect_image.append(img)

load_coin_collect_image(level)

# load health potion image
red_potion = scale_image(pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_image)
item_images.append(red_potion)

# load weapon image
weapon_image = scale_image(pygame.image.load('assets/images/weapons/gun.png').convert_alpha(), constants.GUN_SCALE)
flare_image = scale_image(pygame.image.load('assets/images/weapons/flare.png').convert_alpha(), constants.GUN_SCALE)
fireball_image = scale_image(pygame.image.load('assets/images/weapons/flare.png').convert_alpha(), constants.GUN_SCALE)

# load tile_map images based on current level
tile_list = []

tile_count = constants.TILE_TYPES[level]

for x in range(tile_count):
    tile_image = pygame.image.load(f'{current_asset_path}/images/tiles/{x}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)


# load the character image
mob_animation_list = []
def load_mob_animation_list(level):
    mob_types = constants.LEVEL_CHARACTERS[level]
    animation_types = constants.ANIMATION_TYPES

    for mob in mob_types:
        animation_list = []
        for animation in animation_types:
            temp_list = []
            if mob == "charizard":
                for i in range(8):
                    # Format number with leading zeros (e.g., 000, 001, 002)
                    padded_num = str(i).zfill(3)
                    img = pygame.image.load(f'{current_asset_path}/images/characters/{mob}/{animation}/tile{padded_num}.png').convert_alpha()
                    img = scale_image(img, constants.CHARACTER_SCALE)
                    temp_list.append(img)
                animation_list.append(temp_list)
            else:
                for i in range(4):
                    img = pygame.image.load(f'{current_asset_path}/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
                    img = scale_image(img, constants.CHARACTER_SCALE)
                    temp_list.append(img)
                animation_list.append(temp_list)
        mob_animation_list.append(animation_list)

load_mob_animation_list(level)

# function for text output on screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# function for displaying game info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50), 5)
    #draw lives
    for i in range(5):
        if player.health >= i * 20 + 20:
            screen.blit(heart_full, (10 + i * 50, 0))
        elif player.health >= i * 20 + 10:
            screen.blit(heart_half, (10 + i * 50, 0))
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    #show score
    draw_text(f'Score: {player_score}', font, constants.YELLOW, constants.SCREEN_WIDTH / 2 + 75, 15)

    # level
    draw_text("Level: "+str(level), font, constants.CYAN, constants.SCREEN_WIDTH / 2 - 110, 15)
    #show score
    draw_text(f'X{player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 60, 15)

def draw_grid():
    for x in range (30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))

# function to reset level
def reset_level():
    damage_text_group.empty()
    flare_group.empty()
    item_group.empty()
    fireball_group.empty()

    # create empty tile list
    data = []
    for row in range (constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)

    return data

# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        #repostion the damage text based on scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# class for handling screen fade
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2: #vertical screen fade down 
            pygame.draw.rect(screen, self.colour, (0, 0 , constants.SCREEN_WIDTH, 0 + self.fade_counter))
        
        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

# create empty tile list
world_data = []
for row in range (constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load level data and create world
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animation_list, level)

# create player
player = world.player


# create a weapon object
gun = Weapon(weapon_image, flare_image)

# extract  enemies from world data
enemy_list = world.character_list


# Create sprite group
damage_text_group = pygame.sprite.Group()
flare_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = ItemFactory.create_item(0, constants.SCREEN_WIDTH - 81, 23, coin_collect_image, True)
item_group.add(score_coin)

#add the items from the level data
for item in world.item_list:
    item_group.add(item)

# create screen fades 
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

# create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 70, constants.SCREEN_HEIGHT // 2 - 30, start_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
save_button = Button(constants.SCREEN_WIDTH // 2 - 70, constants.SCREEN_HEIGHT // 2, save_img)
load_button = Button(constants.SCREEN_WIDTH // 2 - 70, constants.SCREEN_HEIGHT // 2 + 70, load_img)
leaderboard_button = Button(constants.SCREEN_WIDTH // 2 - 150, constants.SCREEN_HEIGHT // 2 - 130, leaderboard_img)
back_button = Button(constants.SCREEN_WIDTH // 2 - 80, constants.SCREEN_HEIGHT // 2 + 230, back_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 70, constants.SCREEN_HEIGHT // 2 + 170, exit_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 75, constants.SCREEN_HEIGHT // 2 - 100,resume_img)
level1_button = Button(constants.SCREEN_WIDTH // 2 - 150, constants.SCREEN_HEIGHT // 2 + 50, level1_img)
level2_button = Button(constants.SCREEN_WIDTH // 2 - 50, constants.SCREEN_HEIGHT // 2 + 50, level2_img)
level3_button = Button(constants.SCREEN_WIDTH // 2 + 50, constants.SCREEN_HEIGHT // 2 + 50, level3_img)

def save_game_state(caretaker):
    with open('save_game.json', 'r') as f:
        state = json.load(f)

    level_data = {
        'level1': {
            'player_score': player.score if level == 1 else 0,
            'collected_items': state['level_data']['level1']['collected_items'] + list(world.collected_items) if level == 1 else [],
            'killed_enemies': state['level_data']['level1']['killed_enemies'] + [(enemy.CSV_X, enemy.CSV_Y) for enemy in world.character_list if not enemy.alive] if level == 1 else []
        },
        'level2': {
            'player_score': player.score if level == 2 else 0,
            'collected_items': state['level_data']['level2']['collected_items'] + list(world.collected_items) if level == 2 else [],
            'killed_enemies': state['level_data']['level2']['killed_enemies'] + [(enemy.CSV_X, enemy.CSV_Y) for enemy in world.character_list if not enemy.alive] if level == 2 else []
        },
        'level3': {
            'player_score': player.score if level == 3 else 0,
            'collected_items': state['level_data']['level3']['collected_items'] + list(world.collected_items) if level == 3 else [],
            'killed_enemies': state['level_data']['level3']['killed_enemies'] + [(enemy.CSV_X, enemy.CSV_Y) for enemy in world.character_list if not enemy.alive] if level == 3 else []
        }
    }

    
    memento = GameMemento(
        level=level,
        player_score=player_score,
        player_health=player.health,
        level_data=level_data
    )
    
    caretaker.backup(memento)
    caretaker.save_to_file()

def load_game_state(caretaker):
    memento = caretaker.load_from_file()
    if memento:
        state = memento.get_state()
        return state
    return None

def draw_wrapped_text(text, font, color, x, y, max_width):
    # Split the text into words
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0
    
    # Group words into lines that fit within max_width
    for word in words:
        word_surface = font.render(word + ' ', True, color)
        word_width = word_surface.get_width()
        
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw each line
    line_height = font.get_linesize()
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * line_height))
    
    return len(lines) * line_height  # Return total height of text

def initialize_level(level_number):
    global level, current_asset_path, world_data, tile_list, mob_animation_list, level_complete, coin_collect_image, show_level_intro, player, enemy_list
    level = level_number
    show_level_intro = True
    world_data = reset_level()
    #load level data and create world
    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    # reload tile list for new level
    tile_list = []
    current_asset_path = constants.LEVEL_ASSETS[level]
    tile_count = constants.TILE_TYPES[level]

    for x in range(tile_count):
        tile_image = pygame.image.load(f'{current_asset_path}/images/tiles/{x}.png').convert_alpha()
        tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
        tile_list.append(tile_image)

    mob_animation_list = []
    load_mob_animation_list(level)
    load_audio(level)

    # Reload coin images for current level
    coin_image = []
    img = pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
    img = scale_image(img, constants.ITEM_SCALE)
    coin_image.append(img)
    
    # Reload item images
    item_images = []
    item_images.append(coin_image)
    if len(constants.LEVEL_ITEMS[level]) > 1:
        red_potion = scale_image(pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha(), constants.POTION_SCALE)
        item_images.append(red_potion)
    world = World()
    world.process_data(world_data, tile_list, item_images, mob_animation_list, level)

    player = world.player
    enemy_list = world.character_list
    coin_collect_image = []
    load_coin_collect_image(level)
    score_coin = ItemFactory.create_item(0, constants.SCREEN_WIDTH - 81, 23, coin_collect_image, True)
    item_group.add(score_coin)
    #add the items from the level data, also handles removing items from previous level
    for item in world.item_list:
        item_group.add(item)

def draw_level_intro(screen, level):
    # Draw semi-transparent background
    s = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    s.set_alpha(128)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))
    
    # Calculate popup dimensions
    popup_width = 700
    popup_height = 500
    popup_x = (constants.SCREEN_WIDTH - popup_width) // 2
    popup_y = (constants.SCREEN_HEIGHT - popup_height) // 2


    
    # pygame.draw.rect(screen, constants.PANEL, (popup_x, popup_y, popup_width, popup_height))
    # pygame.draw.rect(screen, constants.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
    
    # Draw title
    title_text = f"Level {level}"
    title_surface = font.render(title_text, True, constants.WHITE)
    title_x = popup_x + (popup_width - title_surface.get_width()) // 2
    screen.blit(title_surface, (title_x, popup_y + 20))
    
    # Draw story text with wrapping (max width of 700 pixels)
    story_height = draw_wrapped_text(constants.LEVEL_STORY[level], font, constants.WHITE, 
                                   popup_x + 50, popup_y + 80, popup_width - 100)
    
    # Calculate vertical position for images based on story text height
    images_y = popup_y + 100 + story_height
    image_spacing = popup_width // 3
    # Load and display enemy image
    enemy_name = constants.LEVEL_CHARACTERS[level][1]
    enemy_img = pygame.image.load(f'assets/level{level}/images/characters/{enemy_name}/idle/0.png').convert_alpha()
    enemy_img = scale_image(enemy_img, constants.CHARACTER_SCALE)
    enemy_x = popup_x + (image_spacing - enemy_img.get_width()) // 2
    screen.blit(enemy_img, (enemy_x, images_y))
    enemy_text = font.render("Enemy", True, constants.WHITE)
    enemy_text_x = popup_x + (image_spacing - enemy_text.get_width()) // 2
    screen.blit(enemy_text, (enemy_text_x, images_y + 100))
    
    # Load and display potion image
    potion_img = pygame.image.load(f'assets/level{level}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha()
    potion_img = scale_image(potion_img, constants.POTION_SCALE)
    potion_x = popup_x + image_spacing + (image_spacing - potion_img.get_width()) // 2
    screen.blit(potion_img, (potion_x, images_y))
    potion_text = font.render("Health", True, constants.WHITE)
    potion_text_x = popup_x + image_spacing + (image_spacing - potion_text.get_width()) // 2
    screen.blit(potion_text, (potion_text_x, images_y + 100))
    
    # Load and display collectible image
    collectible_img = pygame.image.load(f'assets/level{level}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
    collectible_img = scale_image(collectible_img, constants.ITEM_SCALE)
    collectible_x = popup_x + (2 * image_spacing) + (image_spacing - collectible_img.get_width()) // 2
    screen.blit(collectible_img, (collectible_x, images_y))
    collectible_text = font.render("Collectible", True, constants.WHITE)
    collectible_text_x = popup_x + (2 * image_spacing) + (image_spacing - collectible_text.get_width()) // 2
    screen.blit(collectible_text, (collectible_text_x, images_y + 100))
    
    # Draw centered continue text
    continue_text = "Click anywhere to continue"
    continue_surface = font.render(continue_text, True, constants.YELLOW)
    continue_x = popup_x + (popup_width - continue_surface.get_width()) // 2
    screen.blit(continue_surface, (continue_x, popup_y + popup_height ))

def draw_controls_popup(screen):
    # Draw semi-transparent background
    s = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    s.set_alpha(128)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))
    
    # Draw popup box
    popup_width = 400
    popup_height = 320
    popup_x = (constants.SCREEN_WIDTH - popup_width) // 2
    popup_y = (constants.SCREEN_HEIGHT - popup_height) // 2
    
    pygame.draw.rect(screen, constants.PANEL, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, constants.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
    
    # Draw title
    draw_text("Game Controls", font, constants.WHITE, popup_x + 50, popup_y + 20)
    
    # Draw control instructions
    controls = [
        "W - Move Up",
        "S - Move Down",
        "A - Move Left",
        "D - Move Right",
        "Click - Fire",
        "ESC - Pause Game"
    ]
    
    for i, control in enumerate(controls):
        draw_text(control, font, constants.WHITE, popup_x + 50, popup_y + 80 + (i * 30))
    
    # Draw continue text
    draw_text("Click anywhere", font, constants.YELLOW, popup_x + 50, popup_y + 260)
    draw_text(" to continue", font, constants.YELLOW, popup_x + 50, popup_y + 280)

# main game loop
run = True
while run:
    # set the frame rate
    clock.tick(constants.FPS)

    if show_level_intro:
        draw_level_intro(screen, level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_level_intro = False
                show_controls = True

    elif show_input:
        scoreboard.draw_input(screen, total_score)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and scoreboard.input_text:
                    player_name = scoreboard.input_text
                    scoreboard.save_score(player_name, total_score)
                    scoreboard.load_scores()
                    show_input = False
                    show_scoreboard = True
                elif event.key == pygame.K_BACKSPACE:
                    scoreboard.input_text = scoreboard.input_text[:-1]
                else:
                    if len(scoreboard.input_text) < 10:  # Limit name length
                        scoreboard.input_text += event.unicode

    elif show_scoreboard:
        scoreboard.draw_scoreboard(screen)
        if exit_button.draw(screen):
            run = False
    
    elif show_controls:
        draw_controls_popup(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_controls = False
                start_game = True
                start_intro = True

    else:
        if start_game == False:
            screen.fill(constants.MENU_BGCOLOR)
            logo_x = (constants.SCREEN_WIDTH - logo_img.get_width()) // 2
            logo_y = constants.SCREEN_HEIGHT // 4 - 120
            screen.blit(logo_img, (logo_x, logo_y))
            
            if show_leaderboard:
                scoreboard.draw_scoreboard(screen)
                if back_button.draw(screen):
                    show_leaderboard = False
            elif show_level_select:
                if level1_button.draw(screen):
                    show_level_select = False
                    initialize_level(1)
                if level2_button.draw(screen):
                    show_level_select = False
                    initialize_level(2)
                if level3_button.draw(screen):
                    show_level_select = False
                    initialize_level(3)
                if back_button.draw(screen):
                    show_level_select = False
            else:
                if start_button.draw(screen):
                    show_level_select = True
                    
                if leaderboard_button.draw(screen):
                    show_leaderboard = True
                if exit_button.draw(screen):
                    run = False
                if load_button.draw(screen):
                    game_state = load_game_state(game_caretaker)

                    if game_state:
                        player_score = game_state['player_score']
                        level = game_state['level']
                        start_game = True
                        start_intro = True
                        # Initialize world with loaded level
                        world_data = reset_level()
                        
                        # Update current asset path and reload necessary assets for the level
                        current_asset_path = constants.LEVEL_ASSETS[level]
                        
                        # Reload coin images for current level
                        coin_image = []
                        img = pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
                        img = scale_image(img, constants.ITEM_SCALE)
                        coin_image.append(img)
                        
                        # Reload item images
                        item_images = []
                        item_images.append(coin_image)
                        if len(constants.LEVEL_ITEMS[level]) > 1:
                            red_potion = scale_image(pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha(), constants.POTION_SCALE)
                            item_images.append(red_potion)
                        
                        # Reload tile list
                        tile_list = []
                        tile_count = constants.TILE_TYPES[level]
                        for x in range(tile_count):
                            tile_image = pygame.image.load(f'{current_asset_path}/images/tiles/{x}.png').convert_alpha()
                            tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
                            tile_list.append(tile_image)
                            
                        # Load level data
                        with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        mob_animation_list = []
                        load_mob_animation_list(level)
                        load_audio(level)
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animation_list, level)
                        
                        # Get collected items from saved game
                        collected_items = []
                        if game_state and 'collected_items' in game_state['level_data'][f'level{level}']:
                            collected_items = game_state['level_data'][f'level{level}']['collected_items']
                            # Convert collected_items to set of tuples
                            collected_items_set = set(tuple(item) for item in collected_items)
                            world.collected_items = collected_items_set
                            
                            # Remove collected items from world and don't add them to item_group
                            for item in world.item_list[:]:  # Create a copy of the list to iterate
                                if (item.CSV_X, item.CSV_Y) in collected_items_set:
                                    world.item_list.remove(item)
                                else:
                                    item_group.add(item)
                        else:
                            # If no saved collected items, add all items from world
                            for item in world.item_list:
                                item_group.add(item)

                        # Remove killed enemies
                        if 'killed_enemies' in game_state['level_data'][f'level{level}']:
                            killed_enemies = game_state['level_data'][f'level{level}']['killed_enemies']
                            # Convert killed_enemies coordinates to tuples
                            killed_enemies = [tuple(coords) for coords in killed_enemies]
                            # Remove enemies that were killed in the saved game
                            for enemy in world.character_list[:]:
                                if (enemy.CSV_X, enemy.CSV_Y) in killed_enemies:
                                    world.character_list.remove(enemy)
                            enemy_list = world.character_list
                        enemy_list = world.character_list

                        player = world.player
                        player.score = game_state['level_data'][f'level{level}']['player_score']
                        previous_player_score = player.score
                        # Reset and recreate item groups
                        coin_collect_image = []
                        load_coin_collect_image(level)
                        item_group.empty()
                        score_coin = score_coin = ItemFactory.create_item(0, constants.SCREEN_WIDTH - 81, 23, coin_collect_image, True)
                        item_group.add(score_coin)

                        # Get collected items from saved game
                        collected_items = []
                        if game_state and 'collected_items' in game_state['level_data'][f'level{level}']:
                            collected_items = game_state['level_data'][f'level{level}']['collected_items']
                            # Convert collected_items to set of tuples
                            collected_items_set = set(tuple(item) for item in collected_items)
                            world.collected_items = collected_items_set
                            
                            # Remove collected items from world and don't add them to item_group
                            for item in world.item_list[:]:  # Create a copy of the list to iterate
                                if (item.CSV_X, item.CSV_Y) in collected_items_set:
                                    world.item_list.remove(item)
                                else:
                                    item_group.add(item)
                        else:
                            # If no saved collected items, add all items from world
                            for item in world.item_list:
                                item_group.add(item)

                        # Remove killed enemies
                        if 'killed_enemies' in game_state['level_data'][f'level{level}']:
                            killed_enemies = game_state['level_data'][f'level{level}']['killed_enemies']
                            # Convert killed_enemies coordinates to tuples
                            killed_enemies = [tuple(coords) for coords in killed_enemies]
                            # Remove enemies that were killed in the saved game
                            for enemy in world.character_list[:]:
                                if (enemy.CSV_X, enemy.CSV_Y) in killed_enemies:
                                    world.character_list.remove(enemy)
                            enemy_list = world.character_list

            if exit_button.draw(screen):
                run = False

        else:
            if pause_game == True:
                screen.fill(constants.MENU_BGCOLOR)
                if resume_button.draw(screen):
                    pause_game = False
                if save_button.draw(screen):
                    save_game_state(game_caretaker)
                    pause_game = False
                if exit_button.draw(screen):
                    run = False
            else:
                # fill the screen with a color
                screen.fill(constants.BGCOLOR)

                if player.alive:
                    # Calculate the character's movement
                    dx = 0
                    dy = 0
                    if moving_left == True:
                        dx = -constants.CHARACTER_SPEED
                    if moving_right == True:
                        dx = constants.CHARACTER_SPEED
                    if moving_up == True:
                        dy = -constants.CHARACTER_SPEED
                    if moving_down == True:
                        dy = constants.CHARACTER_SPEED

                    # move player
                    screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)


                    # update 
                    world.update(screen_scroll)
                    for enemy in enemy_list:
                        enemy.ai(player, world.obstacle_tiles, screen_scroll)
                        if enemy.alive:
                            isEnemyDead = enemy.update(level)
                            if isEnemyDead:
                                player_score += constants.REWARD_MAP['enemy']

                    player.update()
                    flare = gun.update(player)
                    if flare:
                        flare_group.add(flare)
                        shot_fx.play()
                    for flare in flare_group:
                        damage, damage_pos = flare.update(screen_scroll, world.obstacle_tiles, enemy_list)
                        if damage:
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                            damage_text_group.add(damage_text)
                    damage_text_group.update()
                    fireball_group.update(screen_scroll, player)
                    item_group.update(screen_scroll, player, coin_fx, heal_fx, level, player_score)
                    if player.score != previous_player_score:
                        previous_player_score = player.score
                        player_score += constants.REWARD_MAP['coin']

                # draw the character on screen
                world.draw(screen)
                for enemy in enemy_list:
                    enemy.draw(screen)
                player.draw(screen)
                gun.draw(screen)
                for flare in flare_group:
                    flare.draw(screen)
                damage_text_group.draw(screen)
                item_group.draw(screen)
                draw_info()
                score_coin.draw(screen)

                # check level complete
                if level_complete:
                    # start_intro = True
                    if level == 3:  # Game completed
                        show_input = True
                        total_score = player_score
                        level_complete = False

                    else:
                        level += 1
                        show_level_intro = True
                        world_data = reset_level()
                        #load level data and create world
                        with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        # reload tile list for new level
                        tile_list = []
                        current_asset_path = constants.LEVEL_ASSETS[level]
                        tile_count = constants.TILE_TYPES[level]

                        for x in range(tile_count):
                            tile_image = pygame.image.load(f'{current_asset_path}/images/tiles/{x}.png').convert_alpha()
                            tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
                            tile_list.append(tile_image)

                        mob_animation_list = []
                        load_mob_animation_list(level)
                        load_audio(level)

                        # Reload coin images for current level
                        coin_image = []
                        img = pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][0]}.png').convert_alpha()
                        img = scale_image(img, constants.ITEM_SCALE)
                        coin_image.append(img)
                        
                        # Reload item images
                        item_images = []
                        item_images.append(coin_image)
                        if len(constants.LEVEL_ITEMS[level]) > 1:
                            red_potion = scale_image(pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha(), constants.POTION_SCALE)
                            item_images.append(red_potion)
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animation_list, level)

                        # retain health and score to next level
                        temp_hp = player.health
                        temp_score = player.score
                        player.health = temp_hp
                        player.score = temp_score

                        player = world.player
                        enemy_list = world.character_list
                        coin_collect_image = []
                        load_coin_collect_image(level)
                        score_coin = ItemFactory.create_item(0, constants.SCREEN_WIDTH - 81, 23, coin_collect_image, True)
                        item_group.add(score_coin)
                        #add the items from the level data, also handles removing items from previous level
                        for item in world.item_list:
                            item_group.add(item)

                # show intro
                if start_intro == True:
                    if intro_fade.fade():
                        start_intro = False
                        intro_fade.fade_counter = 0

                # show death screen
                if player.alive == False:
                    if death_fade.fade():
                        if restart_button.draw(screen):
                            death_fade.fade_counter = 0
                            start_intro = True
                            player_score = 0
                            previous_player_score = 0
                            item_group.empty()
                            world_data = reset_level()
                            #load level data and create world
                            with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)

                            # reload tile list for new level
                            tile_list = []
                            current_asset_path = constants.LEVEL_ASSETS[level]
                            tile_count = constants.TILE_TYPES[level]

                            for x in range(tile_count):
                                tile_image = pygame.image.load(f'{current_asset_path}/images/tiles/{x}.png').convert_alpha()
                                tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
                                tile_list.append(tile_image)

                            # Reload item images
                            item_images = []
                            item_images.append(coin_image)
                            if len(constants.LEVEL_ITEMS[level]) > 1:
                                red_potion = scale_image(pygame.image.load(f'{current_asset_path}/images/items/{constants.LEVEL_ITEMS[level][1]}.png').convert_alpha(), constants.POTION_SCALE)
                                item_images.append(red_potion)
                            world = World()
                            world.process_data(world_data, tile_list, item_images, mob_animation_list, level)
                            
                            player = world.player
                            enemy_list = world.character_list
                            score_coin = ItemFactory.create_item(0, constants.SCREEN_WIDTH - 81, 23, coin_collect_image, True)
                            item_group.add(score_coin)
                            #add the items from the level data, also handles removing items from previous level
                            for item in world.item_list:
                                item_group.add(item)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Keydown event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True
        # KeyUp event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()
pygame.quit() 
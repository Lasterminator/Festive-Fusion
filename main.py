import pygame
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button
from scoreboard import Scoreboard


mixer.init()
# initialize pygame
pygame.init() 

# create a screen with a width and height and set the caption
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Halloween Game")

# Clock controlling the speed of the game
clock = pygame.time.Clock()

# define game variables
level = 2
current_asset_path = constants.LEVEL_ASSETS[level]
start_game = False
pause_game = False
start_intro = False
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
scoreboard = Scoreboard()

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# helper function to scale the character image
def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))



# load music and sounds
pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound('assets/audio/arrow_shot.mp3')
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound('assets/audio/arrow_hit.wav')
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound('assets/audio/heal.wav')
heal_fx.set_volume(0.5)

# load button images
start_img = scale_image(pygame.image.load('assets/images/buttons/button_start.png').convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_image(pygame.image.load('assets/images/buttons/button_restart.png').convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_image(pygame.image.load('assets/images/buttons/button_exit.png').convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_image(pygame.image.load('assets/images/buttons/button_resume.png').convert_alpha(), constants.BUTTON_SCALE)
save_img = scale_image(pygame.image.load('assets/images/buttons/button_save.png').convert_alpha(), constants.SAVE_BUTTON_SCALE)
load_img = scale_image(pygame.image.load('assets/images/buttons/button_load.png').convert_alpha(), constants.LOAD_BUTTON_SCALE)
leaderboard_img = scale_image(pygame.image.load('assets/images/buttons/button_leaderboard.png').convert_alpha(), constants.LEADERBOARD_BUTTON_SCALE)
back_img = scale_image(pygame.image.load('assets/images/buttons/button_back.png').convert_alpha(), constants.BUTTON_SCALE)

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
weapon_image = scale_image(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.BOW_SCALE)
arrow_image = scale_image(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.BOW_SCALE)
fireball_image = scale_image(pygame.image.load('assets/images/weapons/fireball.png').convert_alpha(), constants.BOW_SCALE)

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
    arrow_group.empty()
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
bow = Weapon(weapon_image, arrow_image)

# extract  enemies from world data
enemy_list = world.character_list


# Create sprite group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 81, 23, 0, coin_collect_image, True)
item_group.add(score_coin)

#add the items from the level data
for item in world.item_list:
    item_group.add(item)

# create screen fades 
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

# create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 150, start_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
save_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 50, save_img)
load_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 50, load_img)
leaderboard_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 250, leaderboard_img)
back_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 150, back_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 - 150, resume_img)


def save_game_state():
    level1_player_score = 0
    level2_player_score = 0
    level3_player_score = 0
    collected_items = []
    killed_enemies = []

    # Read collected items from temp_save.txt
    try:
        with open('tmp_save.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                if key == 'COLLECTED_ITEMS':
                    collected_items = eval(value)
                elif key == 'KILLED_ENEMIES':
                    killed_enemies = eval(value)
    except FileNotFoundError:
        pass

    # Read existing scores from save file
    try:
        with open('save_game.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                if key == 'level1_player_score':
                    level1_player_score = int(value)
                elif key == 'level2_player_score':
                    level2_player_score = int(value)
                elif key == 'level3_player_score':
                    level3_player_score = int(value)
    except FileNotFoundError:
        pass

    game_state = {
        'level': level,
        'level1_player_score': player.score if level == 1 else level1_player_score,
        'level2_player_score': player.score if level == 2 else level2_player_score,
        'level3_player_score': player.score if level == 3 else level3_player_score,
        'COLLECTED_ITEMS': collected_items,
        'KILLED_ENEMIES': killed_enemies
    }

    with open('save_game.txt', 'w') as f:
        for key, value in game_state.items():
            f.write(f"{key}:{value}\n")

def load_game_state():
    try:
        game_state = {}
        with open('save_game.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                if key == 'COLLECTED_ITEMS' or key == 'KILLED_ENEMIES':
                    # Convert string representation of list to actual list
                    game_state[key] = eval(value)
                else:
                    game_state[key] = int(value)
        return game_state
    except FileNotFoundError:
        return None

# main game loop
run = True
while run:
    # set the frame rate
    clock.tick(constants.FPS)

    if show_input:
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
    else:
        if start_game == False:
            screen.fill(constants.MENU_BGCOLOR)
            
            if show_leaderboard:
                scoreboard.draw_scoreboard(screen)
                if back_button.draw(screen):
                    show_leaderboard = False

            else:
                if start_button.draw(screen):
                    start_game = True
                    start_intro = True
                if leaderboard_button.draw(screen):
                    show_leaderboard = True
                if exit_button.draw(screen):
                    run = False
                if load_button.draw(screen):
                    game_state = load_game_state()

                    if game_state:
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
                            
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animation_list, level)
                        
                        # Remove killed enemies
                        if 'KILLED_ENEMIES' in game_state:
                            for enemy in world.character_list[:]:
                                enemy_x = enemy.CSV_X
                                enemy_y = enemy.CSV_Y
                                if (enemy_x, enemy_y) in game_state['KILLED_ENEMIES']:
                                    world.character_list.remove(enemy)
                        enemy_list = world.character_list

                        player = world.player
                        player.score = game_state[f'level{level}_player_score']
                        
                        # Reset and recreate item groups
                        item_group.empty()
                        score_coin = Item(constants.SCREEN_WIDTH - 81, 23, 0, coin_collect_image, True)
                        item_group.add(score_coin)

                        # Get collected items from saved game
                        collected_items = []
                        if game_state and 'COLLECTED_ITEMS' in game_state:
                            collected_items = game_state['COLLECTED_ITEMS']

                        # Filter out collected items using CSV indices
                        for item in world.item_list[:]:  # Create a copy of the list to iterate
                            if (item.CSV_X, item.CSV_Y) in collected_items:
                                world.item_list.remove(item)
                            else:
                                item_group.add(item)
            if exit_button.draw(screen):
                run = False

        else:
            if pause_game == True:
                screen.fill(constants.MENU_BGCOLOR)
                if resume_button.draw(screen):
                    pause_game = False
                if save_button.draw(screen):
                    save_game_state()
                    pause_game = False
                if exit_button.draw(screen):
                    run = False
            else:
                # fill the screen with a color
                screen.fill(constants.BGCOLOR)

                # draw_grid()

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
                        fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
                        if fireball:
                            fireball_group.add(fireball)
                        if enemy.alive:
                            isEnemyDead = enemy.update()
                            if isEnemyDead:
                                player_score += constants.REWARD_MAP['enemy']

                    player.update()
                    arrow = bow.update(player)
                    if arrow:
                        arrow_group.add(arrow)
                        shot_fx.play()
                    for arrow in arrow_group:
                        damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
                        if damage:
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                            damage_text_group.add(damage_text)
                            hit_fx.play()
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
                bow.draw(screen)
                for arrow in arrow_group:
                    arrow.draw(screen)
                for fireball in fireball_group:
                    fireball.draw(screen)
                damage_text_group.draw(screen)
                item_group.draw(screen)
                draw_info()
                score_coin.draw(screen)

                # check level complete
                if level_complete:
                    start_intro = True
                    if level == 3:  # Game completed
                        show_input = True
                        total_score = player_score
                        level_complete = False

                    else:
                        level += 1
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
                        score_coin = Item(constants.SCREEN_WIDTH - 81, 23, 0, coin_collect_image, True)
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
                            world_data = reset_level()
                            #load level data and create world
                            with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            world.process_data(world_data, tile_list, item_images, mob_animation_list, level)

                            # retain score after death
                            temp_score = player.score
                            player.score = temp_score

                            player = world.player
                            enemy_list = world.character_list
                            score_coin = Item(constants.SCREEN_WIDTH - 81, 23, 0, coin_collect_image, True)
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
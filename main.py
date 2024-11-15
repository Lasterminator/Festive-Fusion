import pygame
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World

# initialize pygame
pygame.init() 

# create a screen with a width and height and set the caption
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Halloween Game")

# Clock controlling the speed of the game
clock = pygame.time.Clock()

# define game variables
level = 1
screen_scroll = [0, 0]

# define character movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# helper function to scale the character image
def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

# load heart image
heart_empty = scale_image(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_image(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_image(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)

# load coin image
coin_image = []
for i in range(4):
    img = pygame.image.load(f'assets/images/items/coin_f{i}.png').convert_alpha()
    img = scale_image(img, constants.ITEM_SCALE)
    coin_image.append(img)

# load health potion image
red_potion = scale_image(pygame.image.load('assets/images/items/potion_red.png').convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_image)
item_images.append(red_potion)

# load weapon image
weapon_image = scale_image(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.BOW_SCALE)
arrow_image = scale_image(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.BOW_SCALE)
fireball_image = scale_image(pygame.image.load('assets/images/weapons/fireball.png').convert_alpha(), constants.BOW_SCALE)

# load tile_map images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f'assets/images/tiles/{x}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)


# load the character image
mob_animation_list = []
mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
animation_types = ['idle', 'run']

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = scale_image(img, constants.CHARACTER_SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animation_list.append(animation_list)

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

    # level
    draw_text("Level: "+str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    #show score
    draw_text(f'X{player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)
 
#create empty tile list
world_data = []
for row in range (constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load level data
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list, item_images, mob_animation_list)

def draw_grid():
    for x in range (30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))

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

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_image, True)
item_group.add(score_coin)

#add the items from the level data
for item in world.item_list:
    item_group.add(item)

# main game loop
run = True
while run:
    # set the frame rate
    clock.tick(constants.FPS)
    # fill the screen with a color
    screen.fill(constants.BGCOLOR)

    draw_grid()

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

    # print(dx, dy)

    # move 
    screen_scroll = player.move(dx, dy, world.obstacle_tiles)
    # print(screen_scroll)

    # update 
    world.update(screen_scroll)
    for enemy in enemy_list:
        fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
        if fireball:
            fireball_group.add(fireball)
        if enemy.alive:
            enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    fireball_group.update(screen_scroll, player)
    item_group.update(screen_scroll, player)

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
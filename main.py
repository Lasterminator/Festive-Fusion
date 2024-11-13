import pygame
import constants
from character import Character
from weapon import Weapon
from items import Item

# initialize pygame
pygame.init() 

# create a screen with a width and height and set the caption
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Halloween Game")

# Clock controlling the speed of the game
clock = pygame.time.Clock()

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

# load weapon image
weapon_image = scale_image(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.BOW_SCALE)
arrow_image = scale_image(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.BOW_SCALE)

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

    #show score
    draw_text(f'X{player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 150, 15)

# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


# create a character object
player = Character(100, 100, 100, mob_animation_list, 0)

# create enemy object
enemy = Character(200, 300, 100, mob_animation_list, 1)

# create a weapon object
bow = Weapon(weapon_image, arrow_image)

# create empty enemy list
enemy_list = []
enemy_list.append(enemy)

# Create sprite group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 165, 23, 0, coin_image)
item_group.add(score_coin)

potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_image)
item_group.add(coin)

# main game loop
run = True
while run:
    # set the frame rate
    clock.tick(constants.FPS)
    # fill the screen with a color
    screen.fill(constants.BGCOLOR)

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

    # move the character
    player.move(dx, dy)

    # update the character's animation
    for enemy in enemy_list:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)

    # draw the character on screen
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
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
import pygame
import constants
from character import Character
from weapon import Weapon

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

# helper function to scale the character image
def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

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

# create a character object
player = Character(100, 100, mob_animation_list, 0)

# create a weapon object
bow = Weapon(weapon_image, arrow_image)

# Create sprite group
arrow_group = pygame.sprite.Group()

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
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        arrow.update()

    # draw the character on screen
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)

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
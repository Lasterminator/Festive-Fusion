import pygame

import input
from player import Player
from sprite import sprites, Sprite
from map import TileKind, Map

# Initialize game
pygame.init()

# Setuip config
pygame.display.set_caption("Adventure Game")
screen = pygame.display.set_mode((800, 600))
clear_color = (0, 0, 0)
running = True
player = Player("assets/player.png", 11 * 32, 10 * 32)
tile_kinds = [
    # TileKind("dirt", "assets/dirt.png", False),
    # TileKind("grass", "assets/grass.png", False),
    TileKind("sand", "assets/sand.png", False),
    TileKind("water", "assets/water.png", False),
    TileKind("wood", "assets/wood.png", False),
]

map = Map("maps/start.map", tile_kinds, 32) #tile size is 32x32
Sprite("assets/tree.png", 10 * 32,10 * 32)

# Game loop
while running:
    for event in pygame.event.get():    #pygame.event contains all the events happing in game
        if event.type == pygame.QUIT:
            print("Player quit is exiting")
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)

    # Update Player
    player.update()

    # Draw
    screen.fill(clear_color)
    map.draw(screen)
    for s in sprites:
        s.draw(screen)

    pygame.display.flip()

    pygame.time.delay(15)   # add a 15 millisec delay

pygame.quit()



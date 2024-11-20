import pygame
import math 
import random
from character import Character
from items import Item
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = []

    def process_data(self, data, tile_list, item_images, mob_animation_list, level):
        self.level_length = len(data)
        # iterate through each value in the data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile in constants.OBSTACLE_TILES_MAP[level]:
                    self.obstacle_tiles.append(tile_data)
                elif tile == constants.EXIT_TILE_MAP[level][0]:
                    self.exit_tile = tile_data
                elif tile == 82:
                    coin = Item(image_x, image_y, 0, item_images[0], False, y, x)
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                elif tile == 84:
                    potion = Item(image_x, image_y, 1, [item_images[1]], False, y, x)
                    self.item_list.append(potion)
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                elif tile == 85:
                    # create a character object
                    player = Character(image_x, image_y, 100, mob_animation_list, 0, False, 1)
                    self.player = player
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                # BOSS
                # elif tile == 17:
                #     enemy = Character(image_x, image_y, 100, mob_animation_list, 6, True, 2, x, y)
                #     self.character_list.append(enemy)
                #     tile_data[0] = tile_list[0]
                elif tile in constants.ENEMY_TILE_MAP[level].values():
                    enemy_name = list(constants.ENEMY_TILE_MAP[level].keys())[0]
                    enemy = Character(image_x, image_y, 100, mob_animation_list, constants.LEVEL_CHARACTERS[level].index(enemy_name), False, 1, y, x)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                #add to map tiles
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
        
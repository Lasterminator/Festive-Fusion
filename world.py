import pygame
import math 
import random
from character import Character
from items import Item
import constants

class World():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        # Initialize all the attributes that were previously in __init__
        self.obstacle_tiles = []
        self.item_list = []
        self.exit_tile = None
        self.player = None
        self.character_list = []
        self.level_length = 0
        self.map_tiles = []
        
    def reset(self):
        """Reset the world state for new level/game"""
        self.obstacle_tiles.clear()
        self.item_list.clear()
        self.exit_tile = None
        self.player = None
        self.character_list.clear()
        self.level_length = 0
        self.map_tiles.clear()

    def process_data(self, data, tile_list, item_images, mob_animation_list, level):
        self.reset()
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
                elif tile == constants.REWARDS_TILES_MAP[level]:
                    coin = Item(image_x, image_y, 0, item_images[0], False, y, x)
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                elif tile == constants.POTIONS_TILES_MAP[level]:
                    potion = Item(image_x, image_y, 1, [item_images[1]], False, y, x)
                    self.item_list.append(potion)
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
                elif tile == constants.CHARACTER_TILE_MAP[level]:
                    # create a character object
                    player = Character(image_x, image_y, 100, mob_animation_list, 0, False, 1)
                    self.player = player
                    tile_data[0] = tile_list[constants.BASE_TILES[level]]
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

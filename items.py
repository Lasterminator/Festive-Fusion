import pygame
import constants
from abc import ABC, abstractmethod

class Item(pygame.sprite.Sprite, ABC):  
    def __init__(self, x, y, animation_list, dummy_coin=False, CSV_X=0, CSV_Y=0):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin
        self.CSV_X = CSV_X
        self.CSV_Y = CSV_Y

    @abstractmethod
    def collect(self, player, player_score, sound_fx):
        pass
    
    def update(self, screen_scroll, player, coin_fx, heal_fx, level, player_score):
        if not self.dummy_coin:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        if self.rect.colliderect(player.rect):
            #coin collected
            if self.item_type == 0:
                player.score += 1
                player_score += constants.REWARD_MAP['coin']
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 20
                heal_fx.play()
                if player.health > 100:
                    player.health = 100
            
            # Add item to world's collected items list
            from world import World
            world = World()
            if not self.dummy_coin:
                world.collected_items.add((self.CSV_X, self.CSV_Y))
                
            self.kill()

        # handle the item animation
        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # def update(self, screen_scroll, player, coin_fx, heal_fx, level, player_score):
    #     #reposition based on screen scroll
    #     if not self.dummy_coin:
    #         self.rect.x += screen_scroll[0]
    #         self.rect.y += screen_scroll[1]

    #     #check if the player collected the item
    #     if self.rect.colliderect(player.rect):
    #         #coin collected
    #         if self.item_type == 0:
    #             player.score += 1
    #             player_score += constants.REWARD_MAP['coin']
    #             coin_fx.play()
    #         elif self.item_type == 1:
    #             player.health += 20
    #             heal_fx.play()
    #             if player.health > 100:
    #                 player.health = 100
    #         # Read existing collected items
    #         existing_items = []
    #         killed_enemies = []
    #         try:
    #             with open('tmp_save.txt', 'r') as f:
    #                 for line in f:
    #                     if line.startswith('COLLECTED_ITEMS:'):
    #                         existing_items = eval(line.split(':')[1])
    #                         break
    #                     elif line.startswith('KILLED_ENEMIES:'):
    #                         killed_enemies = eval(line.split(':')[1])
    #                         break
    #         except FileNotFoundError:
    #             pass

    #         # Add new item if not already collected
    #         if (self.CSV_X, self.CSV_Y) not in existing_items:
    #             existing_items.append((self.CSV_X, self.CSV_Y))
                
    #         # Write back all items
    #         with open('tmp_save.txt', 'w') as f:
    #             f.write(f"COLLECTED_ITEMS:{existing_items}\n")
    #             f.write(f"KILLED_ENEMIES:{killed_enemies}\n")
    #         self.kill()

    #     # handle the item animation
    #     animation_cooldown = 150
    #     self.image = self.animation_list[self.frame_index]
    #     # check if enough time has passed since the last update
    #     if pygame.time.get_ticks() - self.update_time > animation_cooldown:
    #         self.frame_index += 1
    #         self.update_time = pygame.time.get_ticks()
    #     # check if the animation has run out
    #     if self.frame_index >= len(self.animation_list):
    #         self.frame_index = 0

class Coin(Item):
    def collect(self, player, player_score, sound_fx):
        player.score += 1
        player_score += constants.REWARD_MAP['coin']
        sound_fx.play()

class HealthPotion(Item):
    def collect(self, player, player_score, sound_fx):
        player.health = min(player.health + 20, 100)
        sound_fx.play()

class ItemFactory:
    @staticmethod
    def create_item(item_type, x, y, animation_list, dummy_coin=False, CSV_X=0, CSV_Y=0):
        if item_type == 0:  # Coin
            return Coin(x, y, animation_list, dummy_coin, CSV_X, CSV_Y)
        elif item_type == 1:  # Health Potion
            return HealthPotion(x, y, animation_list, dummy_coin, CSV_X, CSV_Y)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
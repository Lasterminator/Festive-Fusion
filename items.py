import pygame
import constants
from abc import ABC, abstractmethod

class Item(pygame.sprite.Sprite, ABC):  
    def __init__(self, x, y, animation_list, dummy_coin=False, CSV_X=0, CSV_Y=0, item_type=0):
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
        self.item_type = item_type

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
            return Coin(x, y, animation_list, dummy_coin, CSV_X, CSV_Y, item_type)
        elif item_type == 1:  # Health Potion
            return HealthPotion(x, y, animation_list, dummy_coin, CSV_X, CSV_Y, item_type)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
import pygame
import math
import random
import constants

class Item(pygame.sprite.Sprite):  
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False, CSV_X = 0, CSV_Y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = coin, 1 = health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin
        self.CSV_X = CSV_X
        self.CSV_Y = CSV_Y
    
    def update(self, screen_scroll, player, coin_fx, heal_fx, level, player_score):
        #reposition based on screen scroll
        if not self.dummy_coin:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        #check if the player collected the item
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
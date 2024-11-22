import pygame
import math 
import random
import constants

class Weapon:
    def __init__(self, image, ammo_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.ammo_image = ammo_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = constants.SHOT_COOLDOWN
        flare = None
        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = (pos[1] - player.rect.centery) * -1 # flip the y-axis for pygame
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # press mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            self.fired = True
            flare = Flare(self.ammo_image, self.rect.centerx, self.rect.centery, self.angle)
            self.last_shot = pygame.time.get_ticks()

        # release mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False
        return flare

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2))))

class Flare(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # calculate the horizontal and vertical speed
        self.dx = math.cos(math.radians(self.angle)) * constants.FLARE_SPEED
        self.dy = (math.sin(math.radians(self.angle)) * constants.FLARE_SPEED) * -1 # flip the y-axis for pygame

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        # reset vars
        damage = 0
        damage_pos = None

        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        #check for collision between flare and tile walls
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check if flare is off screen limit and kill it to save memory
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        # check for collision with enemy
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 25 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2))))


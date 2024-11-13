import pygame
import constants
import math

class Character:
    def __init__(self, x, y, health, mob_animation_list, character_type, boss, size):
        self.character_type = character_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animation_list[character_type]
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.running = True
        self.health = health
        self.alive = True

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
        
    
    # move the character
    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0, 0]
        self.running = False
        # check if the character is running
        if dx != 0 or dy != 0:
            self.running = True
        # flip the character
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False
        # diagonal speed check
        if dx != 0 and dy != 0:
            dx = dx / math.sqrt(2)
            dy = dy / math.sqrt(2)

        # check for collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                elif dx < 0:
                    self.rect.left = obstacle[1].right

        # check for collision with map in y direction
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                elif dy < 0:
                    self.rect.top = obstacle[1].bottom

        # logic only for the player
        if self.character_type == 0:
            # check if the player is out of bounds
            # camera left right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH)
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH

            # camera up down
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH)
        return screen_scroll

    def ai(self, screen_scroll):
        #reposition mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    # update the character's animation
    def update(self):

        # check if the character is alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # check what action the character is doing
        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70

        # handle the animation and update the image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # check if we have run out of frames
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    # update the character's action (walking or running)
    def update_action(self, new_action):
        # check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # draw the character on the screen
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.character_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.CHARACTER_OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)

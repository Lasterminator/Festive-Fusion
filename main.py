import pygame
import sys
import random
import pickle
from pathlib import Path
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 40
ENEMY_SIZE = 30
WHITE = (255, 255, 255)
PLAYER_START_POS = (50, 50)
SAFE_DISTANCE = 150  # Minimum distance from player start position for enemy spawn
SAVE_FILE = Path("game_save.pkl")

# Singleton Pattern for GameManager
class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.score = 0
            cls._instance.level = 1
            cls._instance.player = Player(PLAYER_SIZE)
            cls._instance.level_index = 0
        return cls._instance

    def reset_game(self):
        self.score = 0
        self.level_index = 0
        self.player.reset_position()

    def save_game(self):
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump({'score': self.score, 'level': self.level_index, 'player_pos': self.player.rect.topleft}, f)

    def load_game(self):
        if SAVE_FILE.exists():
            with open(SAVE_FILE, 'rb') as f:
                data = pickle.load(f)
                self.score = data['score']
                self.level_index = data['level']
                self.player.rect.topleft = data['player_pos']

# PowerUp Class
class PowerUp:
    def __init__(self, x, y, effect_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 255, 0)
        self.effect_type = effect_type
        self.duration = 300  # Frames (10 seconds at 30 FPS)

    def apply_effect(self, player):
        if self.effect_type == "speed":
            player.speed_boost = True
        elif self.effect_type == "shield":
            player.shield = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Player Class
class Player:
    def __init__(self, size):
        self.rect = pygame.Rect(*PLAYER_START_POS, size, size)
        self.color = (0, 128, 255)
        self.projectiles = []
        self.speed_boost = False
        self.shield = False
        self.speed = 5

    def move(self, dx, dy):
        if self.speed_boost:
            dx *= 1.5
            dy *= 1.5

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.shield:
            pygame.draw.ellipse(screen, (0, 255, 255), self.rect.inflate(20, 20), 2)

    def reset_position(self):
        self.rect.topleft = PLAYER_START_POS

    def shoot(self, direction):
        projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
        self.projectiles.append(projectile)

    def reset_powerups(self):
        self.speed_boost = False
        self.shield = False

# Projectile Class
class Projectile:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = (255, 255, 0)
        self.speed = 10
        self.direction = direction

    def move(self):
        angle_rad = math.radians(self.direction)
        self.rect.x += self.speed * math.cos(angle_rad)
        self.rect.y += self.speed * math.sin(angle_rad)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Simple particle effect (trail)
        for i in range(1, 5):
            pygame.draw.circle(screen, (255, 165, 0), (self.rect.centerx - int(i * 2), self.rect.centery - int(i * 2)), 2)

# Enemy Class
class Enemy:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 0, 0)
        self.speed = 2

    def chase_player(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Level Base Class (State Pattern)
class Level:
    def __init__(self, theme, goal_color):
        self.theme = theme
        self.obstacles = self.create_obstacles()
        self.enemies = self.create_enemies()
        self.goal = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60, 50, 50)
        self.goal_color = goal_color
        self.power_ups = [PowerUp(random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100), "speed")]

    def create_obstacles(self):
        obstacles = []
        for _ in range(10):  # 10 random obstacles
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            obstacles.append(pygame.Rect(x, y, 50, 50))
        return obstacles
    
    def create_enemies(self):
        enemies = []
        while len(enemies) < 3:  # Create 3 enemies
            x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
            
            # Calculate distance from player's start position
            distance = math.hypot(x - PLAYER_START_POS[0], y - PLAYER_START_POS[1])
            if distance >= SAFE_DISTANCE:
                enemies.append(Enemy(x, y, ENEMY_SIZE))
        return enemies

    def draw(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (100, 0, 0), obstacle)
        for enemy in self.enemies:
            enemy.draw(screen)
        for power_up in self.power_ups:
            power_up.draw(screen)
        pygame.draw.rect(screen, self.goal_color, self.goal)

    def update(self, player):
        for obstacle in self.obstacles:
            if player.rect.colliderect(obstacle):
                return False  # Player hit an obstacle

        for enemy in self.enemies:
            enemy.chase_player(player)
            if player.rect.colliderect(enemy.rect) and not player.shield:
                return False

        for power_up in self.power_ups[:]:
            if player.rect.colliderect(power_up.rect):
                power_up.apply_effect(player)
                self.power_ups.remove(power_up)

        for projectile in player.projectiles[:]:
            projectile.move()
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    player.projectiles.remove(projectile)
                    self.enemies.remove(enemy)
                    GameManager()._instance.score += 5
                    break

            if (projectile.rect.x < 0 or projectile.rect.x > SCREEN_WIDTH or 
                projectile.rect.y < 0 or projectile.rect.y > SCREEN_HEIGHT):
                player.projectiles.remove(projectile)

        if player.rect.colliderect(self.goal):
            return "next_level"
        
        return True

# Specific Levels
class HalloweenLevel(Level):
    def __init__(self):
        super().__init__('Halloween', (150, 0, 150))
        self.background_color = (30, 0, 30)

class ThanksgivingLevel(Level):
    def __init__(self):
        super().__init__('Thanksgiving', (200, 100, 50))
        self.background_color = (139, 69, 19)

class ChristmasLevel(Level):
    def __init__(self):
        super().__init__('Christmas', (0, 200, 0))
        self.background_color = (0, 100, 0)

# Main Menu Function
def main_menu(screen, font):
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render("Holiday Maze Adventure", True, WHITE)
        start_text = font.render("Press 1 to Start New Game", True, WHITE)
        load_text = font.render("Press 2 to Load Game", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        screen.blit(load_text, (SCREEN_WIDTH // 2 - load_text.get_width() // 2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "new_game"
                elif event.key == pygame.K_2:
                    return "load_game"

# Pause Menu Function
def pause_menu(screen, font, game_manager):
    while True:
        screen.fill((0, 0, 0, 128))  # Semi-transparent overlay
        pause_text = font.render("Game Paused", True, WHITE)
        save_text = font.render("Press S to Save Game", True, WHITE)
        exit_text = font.render("Press E to Exit to Main Menu", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 200))
        screen.blit(save_text, (SCREEN_WIDTH // 2 - save_text.get_width() // 2, 300))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_manager.save_game()
                elif event.key == pygame.K_e:
                    return "main_menu"
                elif event.key == pygame.K_ESCAPE:
                    return "resume"

# Main Game Loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Holiday Maze Adventure")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    game_manager = GameManager()

    # Display main menu
    menu_choice = main_menu(screen, font)

    if menu_choice == "load_game":
        game_manager.load_game()

    levels = [HalloweenLevel(), ThanksgivingLevel(), ChristmasLevel()]
    
    running = True
    while running:
        screen.fill(levels[game_manager.level_index].background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_action = pause_menu(screen, font, game_manager)
                    if pause_action == "main_menu":
                        menu_choice = main_menu(screen, font)
                        if menu_choice == "new_game":
                            game_manager.reset_game()
                        elif menu_choice == "load_game":
                            game_manager.load_game()
                elif event.key == pygame.K_SPACE:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx, dy = mouse_x - game_manager.player.rect.centerx, mouse_y - game_manager.player.rect.centery
                    direction = math.degrees(math.atan2(dy, dx))
                    game_manager.player.shoot(direction)

        # Player movement with WASD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            game_manager.player.move(-5, 0)
        if keys[pygame.K_d]:  # Move right
            game_manager.player.move(5, 0)
        if keys[pygame.K_w]:  # Move up
            game_manager.player.move(0, -5)
        if keys[pygame.K_s]:  # Move down
            game_manager.player.move(0, 5)

        # Update and draw level
        level_status = levels[game_manager.level_index].update(game_manager.player)
        if level_status == "next_level":
            game_manager.score += 10
            game_manager.player.reset_position()
            game_manager.level_index = (game_manager.level_index + 1) % len(levels)  # Progress to the next level
        elif not level_status:
            print("Game Over")
            game_manager.reset_game()

        levels[game_manager.level_index].draw(screen)

        # Draw player and projectiles
        game_manager.player.draw(screen)
        for projectile in game_manager.player.projectiles:
            projectile.draw(screen)

        # Draw score and level info
        score_text = font.render(f"Score: {game_manager.score}", True, WHITE)
        level_text = font.render(f"Level: {game_manager.level_index + 1}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

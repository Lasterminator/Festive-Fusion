import json
import pygame
import constants

class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
        self.input_text = ""
        self.scores = ""
        self.input_active = True
        self.load_scores()
        
    def load_scores(self):
        try:
            with open('scoreboard.json', 'r') as f:
                self.scores= json.load(f)['scores']
        except FileNotFoundError:
            return []

    def save_score(self, name, score):
        scores = self.scores
        scores.append({"name": name, "score": score})
        # Sort scores by highest first
        scores.sort(key=lambda x: x['score'], reverse=True)
        # Keep only top 10 scores
        scores = scores[:10]
        
        with open('scoreboard.json', 'w') as f:
            json.dump({"scores": scores}, f, indent=4)

    def draw_input(self, surface, total_score):
        # Draw background
        pygame.draw.rect(surface, constants.MENU_BGCOLOR, (0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        
        # Draw title
        title_text = self.font.render("GAME COMPLETED!", True, constants.WHITE)
        score_text = self.font.render(f"Final Score: {total_score}", True, constants.YELLOW)
        input_prompt = self.font.render("Enter your name:", True, constants.WHITE)
        input_text = self.font.render(self.input_text + "_" if self.input_active else self.input_text, True, constants.WHITE)
        
        surface.blit(title_text, (constants.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        surface.blit(score_text, (constants.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))
        surface.blit(input_prompt, (constants.SCREEN_WIDTH // 2 - input_prompt.get_width() // 2, 250))
        surface.blit(input_text, (constants.SCREEN_WIDTH // 2 - input_text.get_width() // 2, 300))

    def draw_scoreboard(self, surface):
        pygame.draw.rect(surface, constants.MENU_BGCOLOR, (0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        
        title_text = self.font.render("HIGH SCORES", True, constants.WHITE)
        surface.blit(title_text, (constants.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        y_pos = 150
        for i, score in enumerate(self.scores):
            score_text = self.font.render(f"{i+1}. {score['name']}: {score['score']}", True, constants.WHITE)
            surface.blit(score_text, (constants.SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_pos))
            y_pos += 40
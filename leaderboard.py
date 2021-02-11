import pygame.font
import json

class Leaderboard():
    #A class for leaderboard

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)


    def _prep_score_in_leaderboard(self):
        self.leaderboard = 'leaderboard.json'
        with open(self.leaderboard, 'r') as leaderboard_file:
            leaderboard_data = json.load(leaderboard_file)
            high_scores = leaderboard_data['high scores']
            self.names = []
            self.scores = []
            if len(high_scores) > 0:
                for rank in high_scores:
                    self.names.append(f"{rank['name']}")
                    self.scores.append(f"{rank['score']:,}")

    def show_leaderboard(self):
        self._prep_score_in_leaderboard()
        self.leaderboard_title_img = self.font.render("Leaderboard", True, self.text_color, self.settings.bg_color)
        self.leaderboard_title_rect = self.leaderboard_title_img.get_rect()
        self.leaderboard_title_rect.centerx = 500
        self.leaderboard_title_rect.y = 125
        self.screen.blit(self.leaderboard_title_img, self.leaderboard_title_rect)
        for i, name in enumerate(self.names):
            self.name_img = self.font.render(name, True, self.text_color, self.settings.bg_color)
            self.name_rect = self.name_img.get_rect()
            self.name_rect.centerx = 400
            self.name_rect.y = i*50 + 200
            self.screen.blit(self.name_img, self.name_rect)
        for i, score in enumerate(self.scores):
            self.score_img = self.font.render(score, True, self.text_color, self.settings.bg_color)
            self.score_rect = self.score_img.get_rect()
            self.score_rect.centerx = 600
            self.score_rect.y = i*50 + 200
            self.screen.blit(self.score_img, self.score_rect)

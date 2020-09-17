# import pygame.font

# class Leaderboard():
#     #A class for leaderboard

#     def __init__(self, ai_game):
#         self.ai_game = ai_game
#         self.screen = ai_game.screen
#         self.screen_rect = self.screen.get_rect()
#         self.settings = ai_game.settings
#         self.stats = ai_game.stats

#         #Font settings for scoring information
#         self.text_color = (30, 30, 30)
#         self.font = pygame.font.SysFont(None, 48)

#     def prep_leaderboard(self):
#         #Load up the leaderboard data and turn it into a rendered image
#         with open(self.stats.leaderboard, 'r') as leaderboard_file:
#             leaderboard_data = json.load(leaderboard_file)
#             high_scores = leaderboard_data['high scores']
#             for i, rank in enumerate(high_scores):
#                 name_str = f"{rank['name']}"
#                 score_str = "{:,}".format(rank['score'])
#                 self.score_img = self.font.render(score_str, True,
#                 self.text_color, self.settings.bg_color)
#                 self.name_img = self.font.render(name_str, True,
#                 self.text_color, self.settings.bg_color)
#                 #Position the scores starting from rank 1
                
#     def show_leaderboard(self):
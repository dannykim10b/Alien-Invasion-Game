import json

class GameStats:
    #Track statistics for Alien Invasion

    def __init__(self, ai_game):
        #Initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()
    
        #Start Alien Invasion in an inactive state
        self.game_active = False

        #Pause should not be active
        self.pause_active = False

        #Check if game is over
        self.game_over = False

        #High score should never be reset
        self.leaderboard = 'leaderboard.json'
        with open(self.leaderboard) as leaderboard_file:
            leaderboard_data = json.load(leaderboard_file)
            if len(leaderboard_data['high scores']) == 0:
                self.high_score = 0
            else:
                self.high_score = leaderboard_data['high scores'][0]['score']

    def reset_stats(self):
        #Initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
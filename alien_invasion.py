import sys
from time import sleep

import pygame
import json

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from leaderboard import Leaderboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #Overall class to manage game assets and behavior

    def __init__(self):
        #Initialize the game and create game resources
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics
        #And create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.lb = Leaderboard(self)

        #Set background color
        self.bg_color = (230, 230, 230)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button,  resume button, and quit button
        self.play_button = Button(self, "Play")
        self.resume_button = Button(self, "Resume", self.play_button.rect.x, 240)
        self.quit_button = Button(self, "Quit", self.play_button.rect.x, 360)
        self.replay_button = Button(self, "Replay", self.play_button.rect.x, 240)
        self.leaderboard_button = Button(self, "Leaderboard", self.play_button.rect.x, 300)
        self.back_button = Button(self, "Back", self.play_button.rect.x, 450)

    def run_game(self):
        #Start the main loop for the game
        while True:
            self._check_events()

            if not self.stats.pause_active:
                if self.stats.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()

            self._update_screen()

    def _check_events(self):
        #Respond to keypresses and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._leaderboard_update()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_replay_button(mouse_pos)
                    self._check_resume_button(mouse_pos)
                    self._check_quit_button(mouse_pos)
                    self._check_leaderboard_button(mouse_pos)
                    self._check_back_button(mouse_pos)

    def _check_play_replay_button(self, mouse_pos):
        #Start a new game when the player clicks play
        if self.stats.game_over:
            button_clicked = self.replay_button.rect.collidepoint(mouse_pos)
            self._leaderboard_update()
        else:
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            #Reset game stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.game_over = False
            self.sb.prep_images()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_leaderboard_button(self, mouse_pos):
        button_clicked = self.leaderboard_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.pause_active or button_clicked and not self.stats.game_active and self.stats.game_over:
            self.stats.leaderboard_active = True
        pygame.mouse.set_visible(True)

    def _check_back_button(self, mouse_pos):
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.leaderboard_active:
            self.stats.leaderboard_active = False
        # pygame.mouse.set_visible(True)

    def _check_resume_button(self, mouse_pos):
        #Resume game from pause menu
        button_clicked = self.resume_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.pause_active and not self.stats.leaderboard_active:
            self.stats.pause_active = False
        #Hide mouse cursor
        pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.pause_active and not self.stats.leaderboard_active:
            self._leaderboard_update()
            sys.exit()
        if button_clicked and not self.stats.game_active and self.stats.game_over and not self.stats.leaderboard_active:
            sys.exit()
 
    def _check_keydown_events(self, event):
        if not self.stats.pause_active and self.stats.game_active:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_ESCAPE:
                self._open_pause_menu()
        elif self.stats.pause_active and self.stats.game_active:
            if event.key == pygame.K_ESCAPE:
                if self.stats.leaderboard_active:
                    self._esc_to_go_back()
                else:
                    self._close_pause_menu()
        
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _esc_to_go_back(self):
        if self.stats.leaderboard_active:
            self.stats.leaderboard_active = False
        pygame.mouse.set_visible(True)

    def _open_pause_menu(self):
        self.stats.pause_active = True
        #Show mouse cursor
        pygame.mouse.set_visible(True)

    def _close_pause_menu(self):
        self.stats.pause_active = False
        #Hide mouse cursor
        pygame.mouse.set_visible(False)

    def _write_high_score(self, data):
        with open(self.stats.leaderboard, 'w') as leaderboard_file_w:
            json.dump(data, leaderboard_file_w, indent=4)

    def _store_score(self):
        #stores current score as a data
        high_score = {}
        high_score['name'] = "AAA"
        high_score['score'] = round(self.stats.score, -1)
        return high_score

    def _leaderboard_update(self):
        #Updates leaderboard with high scores in a json file
        with open(self.stats.leaderboard, 'r') as leaderboard_file:
            leaderboard_data = json.load(leaderboard_file)
            high_scores = leaderboard_data['high scores']
            if len(high_scores) == 0:
                #Object to be appended is dictionary high_score with key value pair or name and score
                high_scores.append(self._store_score()) 
                self._write_high_score(leaderboard_data)
            else:
                hs_stored = False
                for i, rank in enumerate(high_scores):
                    if self.stats.score >= rank['score']:
                        high_scores.insert(i, self._store_score())
                        hs_stored = True
                        break
                if len(high_scores) < 5 and not hs_stored:
                    high_scores.append(self._store_score()) 
                if len(high_scores) > 5:
                    high_scores.pop()
                self._write_high_score(leaderboard_data)      

    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update bullet positions
        self.bullets.update()

        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #Check for any bullets that have hit aliens
        #If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        self._new_level()

    def _new_level(self):
        #New level conditions when there's no more aliens
        if not self.aliens:
            #Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        #Update the positions of all aliens in the fleet
        #Check if fleet is at an edge before updating positions
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Loof for aliens hitting bottom of screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        #Create a fleet of aliens
        #Create an alien and find number of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            #Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        
        else:
            self.stats.game_active = False
            self.stats.game_over = True
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        #Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #Drop the entire fleet and change the fleets direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        #Check if any aliens have reacehd the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        #Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            #Draw the score information
            self.sb.show_score()

            #Draw the play button if the game is inactive
            if not self.stats.game_active and not self.stats.game_over:
                self.play_button.draw_button()

            #Draw the pause menu when the game is paused
            if self.stats.pause_active and not self.stats.leaderboard_active:
                self.resume_button.draw_button()
                self.quit_button.draw_button()
                self.leaderboard_button.draw_button()

            if self.stats.leaderboard_active:
                self.lb.show_leaderboard()
                self.back_button.draw_button()

            #Draw the replay menu if the game is over
            if not self.stats.game_active and self.stats.game_over and not self.stats.leaderboard_active:
                self.replay_button.draw_button()
                self.quit_button.draw_button()
                self.leaderboard_button.draw_button()

            #Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
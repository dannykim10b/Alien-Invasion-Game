# import pygame.font
# from button import Button

# class Menu:

#     def __init__(self, ai_game, resume_button, quit_button):
#         #Initialize button attributes
#         self.screen = ai_game.screen
#         self.screen_rect = self.screen.get_rect()
#         self.resume_button = resume_button
#         self.quit_button = quit_button

#         self.resume_button.rect.x = self.screen_rect.width/2
#         self.resume_button.rect.y = self.screen_rect.height + self.resume_button.height/2
#         self.quit_button.rect.x = self.screen_rect.width/4
#         self.quit_button.rect.y = self.screen_rect.height - self.quit_button.height/2

#     def draw_menu(self):
#         self.resume_button.draw_button()
#         self.quit_button.draw_button()
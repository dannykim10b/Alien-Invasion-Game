import pygame.font

class Button:

    def __init__(self, ai_game, msg, xpos=0, ypos=0):
        #Initialize button attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set the dimensions and properties of the button
        self.width, self.height = 230, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255 ,255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if not xpos and not ypos:
            self.rect.x = self.screen_rect.width/2 - self.rect.width/2
            self.rect.y = self.screen_rect.height/2 - self.rect.height/2
        else:
            self.rect.x = xpos
            self.rect.y = ypos

        #The button needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #Turns msg into a rendered image and center text on the bottom
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
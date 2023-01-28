import pygame
from sys import exit

class StartMenu:
    def __init__(self):

        # General setup
        self.load_world = False
        self.display_surface = pygame.display.get_surface()
        self.Screen_Width, self.Screen_Height = self.display_surface.get_size()
        self.font = "Comic Sans MS"
        self.font_size = 30
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)


    def display(self):

        # Background color
        sky_bg_color = (172, 156, 255)
        self.display_surface.fill(sky_bg_color)

        # Title font
        vertical_offset = -350
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        my_font = pygame.font.SysFont(self.font, int(self.font_size * 2))
        text_surface = my_font.render('Life in Defense', False, self.black)
        text_horiz_center_offset = text_surface.get_rect()[2] / 2
        text_vert_center_offset = text_surface.get_rect()[3] / 2 + vertical_offset
        self.display_surface.blit(text_surface, (self.Screen_Width / 2 - text_horiz_center_offset, self.Screen_Height / 2 + text_vert_center_offset))


        # New game box
        vertical_offset = -150
        rect_horizontal_pos = self.Screen_Width / 2 - (self.Screen_Width / 4)
        rect_vertical_pos = self.Screen_Height / 2 + vertical_offset
        new_game_rect = pygame.Rect(rect_horizontal_pos, rect_vertical_pos ,self.Screen_Width / 2,100)
        new_game_rect_color = self.black
        new_game_rect_offset = new_game_rect[2] / 2
        pygame.draw.rect(self.display_surface, new_game_rect_color, new_game_rect)

        # New game box font
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        my_font = pygame.font.SysFont(self.font, self.font_size)
        text_surface = my_font.render('New Game', False, self.white)
        text_horiz_center_offset = text_surface.get_rect()[2] / 2
        text_vert_center_offset = text_surface.get_rect()[3] / 2  + vertical_offset
        self.display_surface.blit(text_surface, (self.Screen_Width / 2 - text_horiz_center_offset, self.Screen_Height / 2 + text_vert_center_offset))

        # Load world box
        vertical_offset = 0
        rect_horizontal_pos = self.Screen_Width / 2 - (self.Screen_Width / 4)
        rect_vertical_pos = self.Screen_Height / 2 + vertical_offset
        load_world_rect = pygame.Rect(rect_horizontal_pos, rect_vertical_pos ,self.Screen_Width / 2,100)
        load_world_rect_color = self.black
        load_world_rect_offset = new_game_rect[2] / 2
        pygame.draw.rect(self.display_surface, new_game_rect_color, load_world_rect)

        # Load world  box font
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        my_font = pygame.font.SysFont(self.font, self.font_size)
        text_surface = my_font.render('Load Game', False, self.white)
        text_horiz_center_offset = text_surface.get_rect()[2] / 2
        text_vert_center_offset = text_surface.get_rect()[3] / 2 + vertical_offset
        self.display_surface.blit(text_surface, (self.Screen_Width / 2 - text_horiz_center_offset, self.Screen_Height / 2 + text_vert_center_offset))

        # Quit game box
        vertical_offset = 150
        rect_horizontal_pos = self.Screen_Width / 2 - (self.Screen_Width / 4)
        rect_vertical_pos = self.Screen_Height / 2 + vertical_offset
        quit_game_rect = pygame.Rect(rect_horizontal_pos, rect_vertical_pos ,self.Screen_Width / 2,100)
        quit_game_rect_color = self.black
        quit_game_rect_offset = new_game_rect[2] / 2
        pygame.draw.rect(self.display_surface, quit_game_rect_color, quit_game_rect)

        # Quit game box font
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        my_font = pygame.font.SysFont(self.font, self.font_size)
        text_surface = my_font.render('Quit', False, self.white)
        text_horiz_center_offset = text_surface.get_rect()[2] / 2
        text_vert_center_offset = text_surface.get_rect()[3] / 2 + vertical_offset
        self.display_surface.blit(text_surface, (self.Screen_Width / 2 - text_horiz_center_offset, self.Screen_Height / 2 + text_vert_center_offset))


        # Check if I click on new game
        mpos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]: # Left click
            if new_game_rect.collidepoint(mpos): # Hovering over new game rectangle
                self.load_world = True

            elif load_world_rect.collidepoint(mpos): # Hovering over load game rectangle
                print("Wow much load!")

            elif quit_game_rect.collidepoint(mpos): # Hovering over load game rectangle
                pygame.quit()
                exit()


import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.SysFont("Verdana", 20)
        self.player_position = 1
        self.fps = 1


    def display_debug(self, clock, update_calcs=False):
        text_offset_y = 35
        if update_calcs: # Only update our calculations every x seconds
            self.fps = round(clock.get_fps(), 2)
        self.fps_text = self.font.render(f"FPS: {self.fps}", True, (255, 255, 255))
        self.display_surface.blit(self.fps_text, (50, text_offset_y))
        
        text_offset_y += 35
        if update_calcs: # Only update our calculations every x seconds
            self.player_position = self.player.pos
        self.player_position_text = self.font.render(f"Player Position: {round(self.player_position.x, 1)}, {round(self.player_position.y, 1)}", True, (255, 255, 255))
        self.display_surface.blit(self.player_position_text, (50, text_offset_y))

    def display_inventory(self):
        # Show tools
        # tool_surf = self.tools_surf[self.player.selected_tool]
        # tool_rect = tool_surf.get_rect(midbottom = Overlay_Positions["tool"])
        # self.display_surface.blit(tool_surf, tool_rect)
        pass

import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.SysFont("Verdana", 20)


    def display_debug(self, clock):
        self.text = self.font.render(f"FPS: {round(clock.get_fps(),2)}", True, (255, 255, 255))
        self.display_surface.blit(self.text, (100, 50))

    def display_inventory(self):
        # Show tools
        # tool_surf = self.tools_surf[self.player.selected_tool]
        # tool_rect = tool_surf.get_rect(midbottom = Overlay_Positions["tool"])
        # self.display_surface.blit(tool_surf, tool_rect)
        pass

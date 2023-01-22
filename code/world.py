import pygame
from settings import *

class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()

    def perlin_noise(self, x, y):
        """ Generate a value between 0 and 1.0 
        for perlin noise """

    def load_world(self):
        """ Load all the tiles in the world in """
        # Load a block in
        ground_center = pygame.image.load("../graphics/ground/ground_center.png").convert_alpha()
        ground_top = pygame.image.load("../graphics/ground/ground_top.png").convert_alpha()

        # Loop through entire screen and fill with tiles
        for x in range(0, int(Screen_Tile_Width)):
            for y in range(0, int(Screen_Tile_Height)):
                if y == int(Screen_Tile_Height * 0.8):
                    self.display_surface.blit(ground_top, (x * Tile_Size , y * Tile_Size))
                elif y >= int(Screen_Tile_Height * 0.8):
                    self.display_surface.blit(ground_center, (x * Tile_Size , y * Tile_Size))

    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Load tiles in
        self.load_world()
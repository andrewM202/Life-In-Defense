import pygame
from settings import *
from noise import generate_fractal_noise_2d


class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()
        self.noise = generate_fractal_noise_2d((Screen_Tile_Width, Screen_Tile_Height), (4, 4))

    def load_world(self):
        """ Load all the tiles in the world in """
        # Load a block in
        ground_center = pygame.image.load("../graphics/ground/ground_center.png").convert_alpha()
        ground_top = pygame.image.load("../graphics/ground/ground_top.png").convert_alpha()

        # If we pass this threshold in our 
        # noise generation we are drawing a block
        block_gen_threshold = -0.1
        ground_level = 20

        for x in range(0, Screen_Tile_Width):
            for y in range(0, Screen_Tile_Height):
                if self.noise[x][y] >= block_gen_threshold and y >= ground_level:
                    # If there is no block above make this a top block
                    if y > 0 and self.noise[x][y-1] < block_gen_threshold:
                        self.display_surface.blit(ground_top, (x * Tile_Size , y * Tile_Size))
                    else:
                        self.display_surface.blit(ground_center, (x * Tile_Size , y * Tile_Size))

        # Loop through entire screen and fill with tiles
        # for x in range(0, int(Screen_Tile_Width)):
        #     for y in range(0, int(Screen_Tile_Height)):
        #         if y == int(Screen_Tile_Height * 0.8):
        #             self.display_surface.blit(ground_top, (x * Tile_Size , y * Tile_Size))
        #         elif y >= int(Screen_Tile_Height * 0.8):
        #             self.display_surface.blit(ground_center, (x * Tile_Size , y * Tile_Size))

    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Load tiles in
        self.load_world()
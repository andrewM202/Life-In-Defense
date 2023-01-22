import pygame

class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()

    def load_world(self):
        """ Load all the tiles in the world in """
        # Load a block in

    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Load tiles in
        self.load_world()
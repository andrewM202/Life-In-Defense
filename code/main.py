import pygame
from sys import exit
from settings import *
from world import World

class Game():
    def __init__(self):
        pygame.init()
        flags = 0#pygame.RESIZABLE #| pygame.FULLSCREEN
        # flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((Screen_Width, Screen_Height), flags)
        self.clock = pygame.time.Clock()
		# window title
        pygame.display.set_caption('Life In Defense')
		# Initialize the world
        self.world = World()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            # If the place presses esc close game  
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                exit()


            dt = self.clock.tick() / 1000
			# Run our World
            self.world.run(dt)
            pygame.display.update()

if __name__ == "__main__":
	game = Game()
	game.run()
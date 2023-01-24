import pygame
from sys import exit
from settings import *
from world import World

class Game():
    def __init__(self):
        pygame.init()
        flags = pygame.RESIZABLE# | pygame.FULLSCREEN
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
                if event.type == pygame.WINDOWRESIZED:
                    # Resize to closest interval of tile size
                    x, y = self.screen.get_size()
                    # print(x, y)
                    Screen_Width, Screen_Height = x, y
                    Screen_Tile_Width  = int(round(Screen_Width / Tile_Size))
                    Screen_Tile_Height = int(round(Screen_Height / Tile_Size))
                    Chunk_Tile_Width, Chunk_Tile_Height = Screen_Tile_Width, Screen_Tile_Height
                    Chunk_Pixel_Width, Chunk_Pixel_Height = Chunk_Tile_Width * Tile_Size, Chunk_Tile_Height * Tile_Size
                    print(Screen_Width, Screen_Height)


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
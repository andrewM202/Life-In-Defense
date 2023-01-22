import pygame
from settings import *
from noise import generate_fractal_noise_2d
from player import Player
from sprites import GenericSprite, GroundBlock
from pygame.math import Vector2
import os


class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Chunks
        # Level the ground will spawn at when generating chunks
        self.ground_level = 12
        self.chunks = {}

        # Load tiles in
        self.load_world()

        # Create player
        self.player = Player((600, self.ground_level * Tile_Size), self.all_sprites, self.collision_sprites)

    def load_world(self):
        """ Load all the tiles in the world in """
        # Create our chunks

        for x in range(-1, 1):
            for y in range (0, 1):
                chunk_position = (x, y)
                self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.ground_level, chunk_position)

        # Test delete a chunk
        del self.chunks[(-1, 0)]


    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Draw player
        self.all_sprites.custom_draw(self.player)

        # Update our sprites
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Get position of player, then calculate the offset 
        # of the player into the center of the screen
        self.offset.x = player.rect.centerx - Screen_Width / 2
        self.offset.y = player.rect.centery - Screen_Height / 2
    
        for layer in Layers.values():
            # Loop through all of our sprites, sorting them so player can appear behind
            # objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    # Make a rect of the player's offset then subtract it 
                    # from the sprite's position to make effect of movement
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)


class Chunk():
    def __init__(self, all_sprites, collision_sprites, ground_level = 12, chunk_position=(0 ,0)):
        # How many pxiels wide / tall our chunk is
        self.chunk_pixel_width = Chunk_Tile_Width * Tile_Size
        self.chunk_pixel_height = Chunk_Tile_Height * Tile_Size
        # The level the ground spawns at
        self.ground_level = ground_level

        # Position of the chunk in reference to starting point of (0, 0) in the chunk the player spawns in.
        self.chunk_position = Vector2(chunk_position[0], chunk_position[1])
        # Offset of our chunk
        self.chunk_offset_x = self.chunk_position.x * self.chunk_pixel_width
        self.chunk_offset_y = self.chunk_position.y * self.chunk_pixel_height

        # Sprites
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites

        # Create the noies for the chunk
        self.noise = generate_fractal_noise_2d((Screen_Tile_Width, Screen_Tile_Height), (4, 4))

        # The tiles in our chunk
        self.chunk_tiles = []

        # Generate the chunk
        self.generate()

        # Store our chunk data permanently in a new directory
        self.store_data()

    def __del__(self):
        """ Destructor, free memory """
        pass

    def generate(self):
        """ Generate the actual chunk """
        # Load a block in
        ground_center = pygame.image.load("../graphics/ground/ground_center.png").convert_alpha()
        ground_top = pygame.image.load("../graphics/ground/ground_top.png").convert_alpha()

        # If we pass this threshold in our 
        # noise generation we are drawing a block
        block_gen_threshold = -0.1

        for x in range(0, Screen_Tile_Width):
            for y in range(0, Screen_Tile_Height):
                if self.noise[x][y] >= block_gen_threshold and y >= self.ground_level:
                    # Calculate the local and world coordinates of this tile
                    tile_local_pos = Vector2(x * Tile_Size, y * Tile_Size)
                    tile_world_pos = Vector2(tile_local_pos.x + self.chunk_offset_x, tile_local_pos.y + self.chunk_offset_y)
                    # If there is no block above make this a top block
                    if (y > 0 and self.noise[x][y-1] < block_gen_threshold) or y == self.ground_level:
                        # If no block to the left
                        block = GroundBlock((tile_world_pos.x, tile_world_pos.y), ground_top, [self.all_sprites, self.collision_sprites], Block_Ids["ground_top"])
                        self.chunk_tiles.append(block)
                    else:
                        block = GroundBlock((x * Tile_Size + self.chunk_offset_x, y * Tile_Size + self.chunk_offset_y), ground_center, [self.all_sprites, self.collision_sprites], Block_Ids["ground_center"])
                        self.chunk_tiles.append(block)

    def store_data(self):
        """ Creates the directory used to store the chunk's data permanently """
        try:
            relative_path = f"../world/chunks/{int(self.chunk_position.x)},{int(self.chunk_position.y)}.py"
            # os.mkdir(relative_path)

            # Store our chunk's data
            chunk_file = open(relative_path, "w")

            chunk_file.write("{")

            for tile in self.chunk_tiles:
                # Remove all unnecessary whitespace from the tile so we can reduce
                # storage size when writing to file
                truncated_tile = f"({int(tile.position[0])},{int(tile.position[1])})"
                chunk_file.write(f"{truncated_tile}:{tile.block_id},")

            chunk_file.write("}")

            chunk_file.close()
        except Exception as e:
            print(f"ERROR: {e}")


from settings import *
from noise import generate_fractal_noise_2d
from sprites import GroundBlock
# import pygame
from pygame.sprite import Sprite
from ast import literal_eval # Used for converting our .py chunk files from strings into dictionaries

class Chunk():
    def __init__(self, all_sprites, collision_sprites, block_surfs, ground_level = 6, chunk_position=(0 ,0), load_from_file = False):
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
        
        # Our blocks
        self.blocks = block_surfs

        # The tiles in our chunk
        self.chunk_tiles = []

        if not load_from_file:
            # Create the noies for the chunk
            self.noise = generate_fractal_noise_2d((Screen_Tile_Width, Screen_Tile_Height), (4, 4))

            # Generate the chunk
            self.generate()
        else:
            # Load chunk from file
            self.load_chunk()

    def __del__(self):
        """ Destructor, free memory """
        if Chunk_Logging:
            print(f"Deleting chunk {self.chunk_position.x}, {self.chunk_position.y}")
        for sprite in self.chunk_tiles:
            Sprite.kill(sprite)

    def generate(self):
        """ Generate the actual chunk """
        for x in range(0, Screen_Tile_Width):
            for y in range(0, Screen_Tile_Height):
                if self.noise[x][y] >= Block_Gen_Threshold and (y >= self.ground_level and self.chunk_position.y == 0 or self.chunk_position.y > 0):
                    # Calculate the local and world coordinates of this tile
                    tile_local_pos = Vector2(x * Tile_Size, y * Tile_Size)
                    tile_world_pos = Vector2(tile_local_pos.x + self.chunk_offset_x, tile_local_pos.y + self.chunk_offset_y)

                    # If there is no block above make this a top block
                    if (y > 0 and self.noise[x][y-1] < Block_Gen_Threshold) or y == self.ground_level and self.chunk_position.y == 0:
                        # If no block to the left
                        self.chunk_tiles.append(GroundBlock(
                            position = (tile_world_pos.x, tile_world_pos.y), 
                            surface  = self.blocks[Block_Ids["ground_top"]], 
                            groups   = [self.all_sprites, self.collision_sprites], 
                            block_id = Block_Ids["ground_top"]
                        ))
                    else:
                        self.chunk_tiles.append(GroundBlock(
                            position =  (tile_world_pos.x, tile_world_pos.y), 
                            surface  = self.blocks[Block_Ids["ground_center"]], 
                            groups   = [self.all_sprites, self.collision_sprites], 
                            block_id = Block_Ids["ground_center"]
                        ))
        
        # Store the chunk data in a file
        self.store_data()

    def load_chunk(self):
        """ Load the chunk from a file """
        relative_path = f"../world/chunks/{int(self.chunk_position.x)},{int(self.chunk_position.y)}.py"

        # Retrieve our chunk's data
        chunk_file = open(relative_path, "r")

        chunk_data = literal_eval(chunk_file.read())

        for tile in chunk_data:
            # Calculate the local and world coordinates of this tile
            tile_world_pos = Vector2(tile[0], tile[1])

            # Create our block
            block = GroundBlock(
                position = (tile_world_pos.x, tile_world_pos.y), 
                surface  = self.blocks[chunk_data[tile]],
                groups   = [self.all_sprites, self.collision_sprites], 
                block_id = Block_Ids["ground_top"]
            )
            self.chunk_tiles.append(block)

        # Close our file!
        chunk_file.close()

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

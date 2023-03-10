from settings import *
from noise import generate_fractal_noise_2d
from sprites import GroundBlock
# import pygame
from pygame.sprite import Sprite
from ast import literal_eval # Used for converting our .py chunk files from strings into dictionaries
from random import choice
from threading import Thread
from json import dumps # Turn our tile dictionary into a string

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
        self.chunk_tiles = {}
        # The sprites in our chunk
        self.chunk_sprites = {}

        if not load_from_file:
            # Create the noies for the chunk
            self.noise = generate_fractal_noise_2d((Chunk_Tile_Width, Chunk_Tile_Height), (12, 12), 1)
            # print(self.noise)
            self.height_map = generate_fractal_noise_2d((Screen_Tile_Width, 2), (2, 2))

            # Generate the chunk
            self.generate()

            # Store the chunk data in a file
            # self.store_data()
            Thread(target=self.store_data, args=()).start()
        else:
            # Load chunk from file
            self.load_chunk()

    def __del__(self):
        """ Destructor, free memory """
        if Chunk_Logging:
            print(f"Deleting chunk {self.chunk_position.x}, {self.chunk_position.y}")
        for sprite in self.chunk_sprites.values():
            Sprite.kill(sprite)

    def generate(self):
        """ Generate the actual chunk """
        for x in range(0, Screen_Tile_Width):
            self.ground_level = int(self.height_map[x][0] * 16)
            for y in range(0, Screen_Tile_Height):
                if self.noise[x][y] >= Block_Gen_Threshold and y * Tile_Size + self.chunk_offset_y >= self.ground_level:
                    # Calculate the local and world coordinates of this tile
                    tile_local_pos = (x * Tile_Size, y * Tile_Size)
                    tile_world_pos = (tile_local_pos[0] + self.chunk_offset_x, tile_local_pos[1] + self.chunk_offset_y)

                    # If there is no block above make this a top block
                    if not (self.noise[x][y-1] >= Block_Gen_Threshold and (y-1) * Tile_Size + self.chunk_offset_y >= self.ground_level):
                        try:
                            # If no block to the left
                            block_left = self.noise[x-1][y] >= Block_Gen_Threshold and y * Tile_Size + self.chunk_offset_y >= int(self.height_map[x-1][0] * 16)
                            block_right = self.noise[x+1][y] >= Block_Gen_Threshold and y * Tile_Size + self.chunk_offset_y >= int(self.height_map[x+1][0] * 16)

                            if not block_left and not block_right:
                                self.chunk_sprites[tile_world_pos] = GroundBlock(
                                    position = tile_world_pos, 
                                    surface  = self.blocks[Block_Ids["ground_top_padded"]], 
                                    groups   = [self.all_sprites, self.collision_sprites], 
                                    block_id = Block_Ids["ground_top_padded"]
                                )
                                self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top_left"]
                            elif not block_left:
                                self.chunk_sprites[tile_world_pos] = GroundBlock(
                                    position = tile_world_pos, 
                                    surface  = self.blocks[Block_Ids["ground_top_left"]], 
                                    groups   = [self.all_sprites, self.collision_sprites], 
                                    block_id = Block_Ids["ground_top_left"]
                                )
                                self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top_left"]
                            # If no block to the right
                            elif not block_right:
                                self.chunk_sprites[tile_world_pos] = GroundBlock(
                                    position = tile_world_pos, 
                                    surface  = self.blocks[Block_Ids["ground_top_right"]], 
                                    groups   = [self.all_sprites, self.collision_sprites], 
                                    block_id = Block_Ids["ground_top_right"]
                                )
                                self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top_right"]
                            # Else just top middle
                            else:
                                self.chunk_sprites[tile_world_pos] = GroundBlock(
                                    position = tile_world_pos, 
                                    surface  = self.blocks[Block_Ids["ground_top"]], 
                                    groups   = [self.all_sprites, self.collision_sprites], 
                                    block_id = Block_Ids["ground_top"]
                                )
                                self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top"]
                        except Exception as e:
                            self.chunk_sprites[tile_world_pos] = GroundBlock(
                                position = tile_world_pos, 
                                surface  = self.blocks[Block_Ids["ground_top"]], 
                                groups   = [self.all_sprites, self.collision_sprites], 
                                block_id = Block_Ids["ground_top"]
                            )
                            self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top"]
                    else:
                        # Pick a random center ground variant
                        id = f"ground_center_{choice([1, 1, 1, 1, 2, 3, 4])}"
                        self.chunk_sprites[tile_world_pos] = GroundBlock(
                            position =  tile_world_pos, 
                            surface  = self.blocks[Block_Ids[id]], 
                            groups   = [self.all_sprites, self.collision_sprites], 
                            block_id = Block_Ids[id]
                        )
                        self.chunk_tiles[tile_world_pos] = Block_Ids[id]

        # Make corner blocks correct
        for position, block_id in self.chunk_tiles.items():
            if block_id in [1, 2, 3, 4]: # Its a ground center variant
                try:
                    if(
                        # The block above is grass
                        self.chunk_tiles[(position[0], position[1]-Tile_Size)] in [0, 5, 6]
                        # The block to the left is grass
                        and self.chunk_tiles[(position[0]-Tile_Size, position[1])] in [0, 5, 6]
                    ):
                        Sprite.kill(self.chunk_sprites[position])
                        self.chunk_sprites[tile_world_pos] = GroundBlock(
                            position =  position, 
                            surface  = self.blocks[Block_Ids["ground_center_top_left"]], 
                            groups   = [self.all_sprites, self.collision_sprites], 
                            block_id = Block_Ids["ground_center_top_left"]
                        )
                        # self.chunk_sprites[position].surface = self.blocks[Block_Ids["ground_center_top_left"]]
                        # self.chunk_sprites[position].block_id = Block_Ids["ground_center_top_left"]
                        self.chunk_tiles[position] = Block_Ids["ground_center_top_left"]
                except Exception as e:
                    pass
                try:
                    if(
                        # The block above is grass
                        self.chunk_tiles[(position[0], position[1]-Tile_Size)] in [0, 5, 6]
                        # The block to the right is grass
                        and self.chunk_tiles[(position[0]+Tile_Size, position[1])] in [0, 5, 6]
                    ):
                        Sprite.kill(self.chunk_sprites[position])
                        self.chunk_sprites[tile_world_pos] = GroundBlock(
                            position =  position, 
                            surface  = self.blocks[Block_Ids["ground_center_top_right"]], 
                            groups   = [self.all_sprites, self.collision_sprites], 
                            block_id = Block_Ids["ground_center_top_right"]
                        )
                        # self.chunk_sprites[position].surface = self.blocks[Block_Ids["ground_center_top_left"]]
                        # self.chunk_sprites[position].block_id = Block_Ids["ground_center_top_left"]
                        self.chunk_tiles[position] = Block_Ids["ground_center_top_right"]
                except Exception as e:
                    pass
        
    def load_chunk(self):
        """ Load the chunk from a file """
        relative_path = f"../world/chunks/{int(self.chunk_position.x)},{int(self.chunk_position.y)}.py"

        # Retrieve our chunk's data
        chunk_file = open(relative_path, "r")

        chunk_data = literal_eval(chunk_file.read())

        for tile in chunk_data:
            # Calculate the local and world coordinates of this tile
            tile_world_pos = (tile[0], tile[1])

            # Create our block
            self.chunk_sprites[tile_world_pos] = GroundBlock(
                position = tile_world_pos, 
                surface  = self.blocks[chunk_data[tile]],
                groups   = [self.all_sprites, self.collision_sprites], 
                block_id = Block_Ids["ground_top"]
            )
            self.chunk_tiles[tile_world_pos] = Block_Ids["ground_top"]

        # Close our file!
        chunk_file.close()

    def store_data(self):
        """ Creates the directory used to store the chunk's data permanently """
        # try:
        relative_path = f"../world/chunks/{int(self.chunk_position.x)},{int(self.chunk_position.y)}.py"
        # os.mkdir(relative_path)

        # Store our chunk's data
        chunk_file = open(relative_path, "w")

        chunk_file.write("{")

        for position, block_id in self.chunk_tiles.items():
            # Remove all unnecessary whitespace from the tile so we can reduce
            # storage size when writing to file
            truncated_tile = f"({int(position[0])},{int(position[1])})"
            chunk_file.write(f"{truncated_tile}:{block_id},")

        chunk_file.write("}")

        chunk_file.close()
        # except Exception as e:
        #     print(f"ERROR: {e}")

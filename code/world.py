import pygame
from settings import *
from player import Player
from chunk import Chunk
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

        # Load blocks
        self.blocks = {}
        self.load_blocks()

        # Load tiles in
        self.load_world()

        # Create player
        self.player = Player((600, self.ground_level * Tile_Size), self.all_sprites, self.collision_sprites)

    def load_blocks(self):
        """ Load all of our blocks in as surfaces """
        for block in Block_Ids:
            self.blocks[Block_Ids[block]] = pygame.image.load(f"../graphics/ground/{block}.png").convert_alpha()

    def load_world(self):
        """ Load all the tiles in the world in """
        # Create our chunks

        for x in range(-1, 1):
            for y in range (0, 1):
                chunk_position = (x, y)
                self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position)

        # # Test delete a chunk
        # chunk_position = (-1, 0)
        # # self.chunks[chunk_position].__del__()
        # del self.chunks[chunk_position] # Free memory

        # # Test restore the chunk
        # self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, True)

    def manage_chunks(self):
        """ Remove or load chunks from memory depending
        on proximity to player """

        player_position = self.player.hitbox.center

        # print(len(self.chunks))

        # Delete Chunks

        # Have a list of chunks we want to delete
        chunks_to_delete = []

        for key in self.chunks.keys():
            player_chunk_distance = max([
                abs(player_position[0] - (key[0] * Chunk_Tile_Width * Tile_Size)),
                abs(player_position[0] - ((key[0] + 1 ) * Chunk_Tile_Width * Tile_Size))
            ])

            if player_chunk_distance > Screen_Width * 2.5:
                # If the chunk crosses the threshold, add it to delete.
                # We can't delete it here; will cause an error since we would be
                # deleting from self.chunks while we are looping through it
                chunks_to_delete.append(key)

        for key in chunks_to_delete:
            del self.chunks[key]

        # Restore chunks that are within 2 screen widths of the player
        chunks_range_x = (player_position[0] - (2 * Screen_Width), player_position[0] + (2 * Screen_Width)) 
        chunks_to_load = []

        for i in range(player_position[0], chunks_range_x[0], -Chunk_Pixel_Width):
            chunks_to_load.append((round(i / Chunk_Pixel_Width), 0))

        for i in range(player_position[0], chunks_range_x[1], Chunk_Pixel_Width):
            chunks_to_load.append((round(i / Chunk_Pixel_Width), 0))

        for chunk_position in chunks_to_load:
            if chunk_position not in self.chunks:
                # Check if the file for this chunk already exists
                relative_path = f"../world/chunks/{int(chunk_position[0])},{int(chunk_position[1])}.py"
                isExist = os.path.exists(relative_path)

                # print(f"Restoring chunk: {chunk_position}")
                # print(chunks_to_load)
                # print()

                if isExist:
                    self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, True)
                else:
                    self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, False)
                


    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Draw player
        self.all_sprites.custom_draw(self.player)

        # Manage our chunks
        self.manage_chunks()

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




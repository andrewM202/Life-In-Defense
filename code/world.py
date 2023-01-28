import pygame
from settings import *
from player import Player
from chunk import Chunk
from pygame.math import Vector2
from os import listdir, remove, path
from sprites import GroundBlock
from random import choice



class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Chunks
        # Level the ground will spawn at when generating chunks
        self.ground_level = 12
        self.chunks = {}

        # Background
        self.bg = pygame.image.load("../graphics/background/background_glacial_mountains.png").convert_alpha()
        # self.bg = pygame.image.load("../graphics/background/forest.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (Screen_Width, Screen_Height))

        # Load blocks
        self.blocks = {}
        self.load_blocks()

        # Sprite groups
        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.all_sprites.set_attributes(self.collision_sprites, self.all_sprites, self.blocks)

        # Create player
        self.player = Player((0, 0), self.all_sprites, self.collision_sprites)

        # Reset world for now by deleting all files in chunks folder, will delete later
        if New_World:
            path = "../world/chunks/"
            for file in listdir(path):
                remove(path + file)

    def load_blocks(self):
        """ Load all of our blocks in as surfaces """
        for block in Block_Ids:
            self.blocks[Block_Ids[block]] = pygame.image.load(f"../graphics/ground/{block}.png").convert_alpha()


    def manage_chunks(self):
        """ Remove or load chunks from memory depending
        on proximity to player """

        player_position = self.player.hitbox.center

        # Delete Chunks

        # Have a list of chunks we want to delete
        chunks_to_delete = []

        for key in self.chunks.keys():
            player_chunk_distance_width = max([
                abs(player_position[0] - (key[0] * Chunk_Tile_Width * Tile_Size)),
                abs(player_position[0] - ((key[0] + 1 ) * Chunk_Tile_Width * Tile_Size))
            ])

            if player_chunk_distance_width > Screen_Width * 2:
                # If the chunk crosses the threshold, add it to delete.
                # We can't delete it here; will cause an error since we would be
                # deleting from self.chunks while we are looping through it
                chunks_to_delete.append(key)

            player_chunk_distance_height = max([
                abs(player_position[1] - (key[1] * Chunk_Tile_Height * Tile_Size)),
                abs(player_position[1] - ((key[1] + 1 ) * Chunk_Tile_Height * Tile_Size))
            ])

            if player_chunk_distance_height > Screen_Height * 2:
                # If the chunk crosses the threshold, add it to delete.
                # We can't delete it here; will cause an error since we would be
                # deleting from self.chunks while we are looping through it
                chunks_to_delete.append(key)

        # Delete the selected chunks from memory
        for key in chunks_to_delete:
            del self.chunks[key]

        # Restore chunks that are within 2 screen widths or heights of the player
        chunks_range_x = (player_position[0] - int(0.6 * Screen_Width), player_position[0] + int(0.6 * Screen_Width)) 
        chunks_range_y = (player_position[1] - int(0.6 * Screen_Height), player_position[1] + int(0.6 * Screen_Height)) 
        chunks_to_load = []
        # print(player_position[0], chunks_range_x[0])
        # for x in range(player_position[0], chunks_range_x[0], -Chunk_Pixel_Width):
        #     for y in range(player_position[1], chunks_range_y[0], -Chunk_Pixel_Height):
        for x in range(chunks_range_x[0], chunks_range_x[1], Chunk_Pixel_Width):
            for y in range(chunks_range_y[0], chunks_range_y[1], Chunk_Pixel_Height):
                chunk_pos = (round(x / Chunk_Pixel_Width), round(y / Chunk_Pixel_Height))
                if chunk_pos not in chunks_to_load:
                    chunks_to_load.append((round(x / Chunk_Pixel_Width), round(y / Chunk_Pixel_Height)))

        for chunk_position in chunks_to_load:
            if chunk_position not in self.chunks:
                # Check if the file for this chunk already exists
                relative_path = f"../world/chunks/{int(chunk_position[0])},{int(chunk_position[1])}.py"
                fileAlreadyExists = path.exists(relative_path)

                if fileAlreadyExists:
                    self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, True)
                    if Chunk_Logging:
                        print(f"Restoring chunk: {chunk_position}")
                        str = ""
                        for pos in self.chunks: str+= f"{pos}, "
                        print(str)
                else:
                    self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, False)
                    if Chunk_Logging:
                        print(f"Creating chunk: {chunk_position}")
                        str = ""
                        for pos in self.chunks: str+= f"{pos}, "
                        print(str)
                


    def run(self, dt):
        # Set background
        # sky_bg_color = (92, 76, 255)
        # self.display_surface.fill(sky_bg_color)
        self.display_surface.blit(self.bg, (0, 0))

        # Draw player
        # self.all_sprites.custom_draw(self.player, self.collision_sprites, self.all_sprites, self.blocks)
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

    def set_attributes(self, collision_sprites, all_sprites, blocks):
        self.collision_sprites = collision_sprites
        self.all_sprites = all_sprites
        self.blocks = blocks

    # def custom_draw(self, player, collision_sprites, all_sprites, blocks):
    def custom_draw(self, player):
        """ This method draws the sprites in the correct order
        and handles block placement / breaking """

        # Get position of player, then calculate the offset 
        # of the player into the center of the screen
        self.offset.x = player.rect.centerx - Screen_Width / 2
        self.offset.y = player.rect.centery - Screen_Height / 2

        window_left_border = player.rect.centerx - (Screen_Width / 2) - Tile_Size
        window_top_border = player.rect.centery - (Screen_Height / 2) - Tile_Size

        window_rect = pygame.Rect(window_left_border, window_top_border, Screen_Width + Tile_Size, Screen_Height + Tile_Size)

        for layer in Layers.values():
            # Loop through all of our sprites, sorting them so player can appear behind
            # objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                # Check if this sprite is off window; if it is don't draw it
                if self.collision_sprites.has(sprite):
                    if not window_rect.collidepoint(sprite.position):
                        continue
                if sprite.z == layer:
                    # Make a rect of the player's offset then subtract it 
                    # from the sprite's position to make effect of movement
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # BLOCK BREAKING
                    if offset_rect.collidepoint((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) and self.collision_sprites.has(sprite):
                        sprite.mouse_hover = True
                        # Create mask for sprite
                        mask = pygame.mask.from_surface(sprite.image)
                        for point in mask.outline():
                            # print(sprite.image.get_height())
                            x = point[0] + offset_rect.x
                            y = point[1] + offset_rect.y
                            pygame.draw.circle(pygame.display.get_surface(), "gray", (x,y), 2)

                        # If mouseover and click delete block
                        if pygame.mouse.get_pressed()[0]: # Left click
                            pygame.sprite.Sprite.kill(sprite)

                        if pygame.mouse.get_pressed()[2]: # Riight click
                            # Pick a random blocks
                            id = choice([i for i in Block_Ids.values()])
                            for block in Block_Ids.items():
                                if block[1] == id:
                                    id = block[0]
                            pygame.sprite.Sprite.kill(sprite)
                            GroundBlock(
                                position =  (sprite.position[0], sprite.position[1]), 
                                surface  = self.blocks[Block_Ids[id]], 
                                groups   = [self.all_sprites, self.collision_sprites], 
                                block_id = Block_Ids[id]
                            )
                            sprite.surface = self.blocks[Block_Ids[id]]
                            sprite.block_id = Block_Ids[id]
                            
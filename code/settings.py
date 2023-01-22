# Settings here

from pygame.math import Vector2

# Screen height, width
Screen_Width, Screen_Height = 1280, 768
# Pixel size of each tile
Tile_Size = 32

# How many tiles fill up the screen
Screen_Tile_Width  = int(round(Screen_Width / Tile_Size))
Screen_Tile_Height = int(round(Screen_Height / Tile_Size))

# How many tiles are in a chunk
Chunk_Tile_Width, Chunk_Tile_Height = Screen_Tile_Width, Screen_Tile_Height


Layers = {
    "ground": 0,
    "player": 1
}
# Settings here

import tkinter
from pygame.math import Vector2

root = tkinter.Tk()
root.withdraw()

# Resolution
Screen_Width, Screen_Height = root.winfo_screenwidth(), root.winfo_screenheight()
Screen_Width, Screen_Height = 1280, 720
# Screen_Width, Screen_Height = 1600, 900
# resolution = Screen_Width / Screen_Height
# Screen_Width = Screen_Height * resolution
# Pixel size of each tile
Tile_Size = 32

# How many tiles fill up a chunk
Screen_Tile_Width  = int(round(768 /2 / Tile_Size))
Screen_Tile_Height = int(round(768 /2 / Tile_Size))

# How many tiles are in a chunk
Chunk_Tile_Width, Chunk_Tile_Height = Screen_Tile_Width, Screen_Tile_Height
Chunk_Pixel_Width, Chunk_Pixel_Height = Chunk_Tile_Width * Tile_Size, Chunk_Tile_Height * Tile_Size
# Chunk logging
Chunk_Logging = False

Layers = {
    "ground": 0,
    "player": 1
}

Block_Ids = {
    "ground_top": None,
    "ground_center_1": None,
    "ground_center_2": None,
    "ground_center_3": None,
    "ground_center_4": None,
    "ground_top_left": None,
    "ground_top_right": None,
    "ground_center_top_left": None,
    "ground_center_top_right": None,
    "ground_center_bottom_left": None,
    "ground_center_bottom_right": None,
    "ground_top_padded": None,
}

index = 0
for block_id in Block_Ids:
    Block_Ids[block_id] = index
    index += 1

New_World = True

# How often caves spawn. Lower number == less caves
Block_Gen_Threshold = -0.5

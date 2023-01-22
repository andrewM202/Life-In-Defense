from os import walk, sep # Walk to walk through different folders
import pygame

def import_folder(path):
    """ Import our graphical assets """
    surface_list = []

    for folder_name, sub_folders, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            # Always convert alpha to work easier with python
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)


    return surface_list

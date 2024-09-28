from os import path
from pygame.image import load

def get_path(name: str):
    return path.normpath(path.join(__file__, f"../../assets/sprites/{name}.png"))

def load_sprite(name: str):
    return load(get_path(name)).convert()

def load_sprite_alpha(name: str):
    return load(get_path(name)).convert_alpha()

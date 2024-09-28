from os import path
from pygame import Surface
from pygame.image import load

def _get_surface(name: str):
    """
    Renvoie la surface associée a un nom de sprite.
    """
    return load(path.join("assets", "sprites", f"{name}.png"))

def load_sprite(name: str) -> Surface:
    """
    Renvoie la surface associée a un nom de sprite sans alpha.
    """
    return _get_surface(name).convert()

def load_sprite_alpha(name: str) -> Surface:
    """
    Renvoie la surface associée a un nom de sprite avec alpha.
    """
    return _get_surface(name).convert_alpha()

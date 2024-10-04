from os import path

from pygame import Surface
from pygame.image import load
from pygame.mixer import Sound


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


def load_sound(name: str, volume: float = 1.0) -> Sound:
    sound = Sound(path.join("assets", "sounds", name))
    sound.set_volume(volume)
    return sound

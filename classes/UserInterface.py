import pygame.freetype
from pygame import Surface

from utils.assets import load_sprite_alpha
from utils.consts import SCREEN_SIZE

pygame.freetype.init()


class UserInterface:
    def __init__(self) -> None:
        self.gamefont24 = pygame.freetype.Font(
            file="./assets/PressStart2P-Regular.ttf", size=24
        )
        self.heart = load_sprite_alpha("heart")
        self.lives = 3
        self.level = 0

    @property
    def alive(self):
        return True

    def draw(self, surface: Surface):
        self.gamefont24.render_to(
            surface, (40, 40), f"Niveau {self.level}", (255, 0, 0)
        )

        width = self.heart.get_width()
        for i in range(self.lives):
            surface.blit(self.heart, (SCREEN_SIZE[0] - 2 * width - (i + 1) * width, 56))

    def tick(self, deltaTime: float):
        pass

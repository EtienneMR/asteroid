import pygame.freetype
from pygame import Surface

pygame.freetype.init()

class UserInterface:
    def __init__(self) -> None:
        self.gamefont24 = pygame.freetype.Font(
            file="./assets/PressStart2P-Regular.ttf",
            size=24
        )
        self.level = 0

    @property
    def alive(self):
        return True

    def draw(self, surface: Surface):
        self.gamefont24.render_to(surface, (40, 40), f"Niveau {self.level}", (255, 0, 0))

    def tick(self, deltaTime: float):
        pass
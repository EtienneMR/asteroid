from typing import Protocol

from pygame import Surface


class IRenderable(Protocol):
    alive: bool

    def draw(self, surface: Surface):
        pass

    def tick(self, deltaTime: float):
        pass
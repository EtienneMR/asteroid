from pygame import Rect, Surface, Vector2

from entities.BaseEntity import BaseEntity
from utils.assets import load_sprite_alpha
from utils.consts import SCREEN_SIZE

FRAMES = 24
TOTAL_TIME = 2.0
FRAME_SIZE = 128


class Explosion(BaseEntity):
    def __init__(self, position: Vector2):
        super().__init__(sprite=load_sprite_alpha("explosion"), position=position)

        self.time = 0.0

    def tick(self, deltaTime: float):
        self.time += deltaTime
        if self.time > TOTAL_TIME:
            self.alive = False
        return super().tick(deltaTime)

    def draw(self, surface: Surface):
        surface.blit(
            self.sprite,
            self.position - Vector2(FRAME_SIZE, FRAME_SIZE) / 2,
            Rect(
                FRAME_SIZE * int(self.time / TOTAL_TIME * FRAMES),
                0,
                FRAME_SIZE,
                FRAME_SIZE,
            ),
        )

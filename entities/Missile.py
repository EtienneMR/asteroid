from pygame import Vector2

from entities.BaseEntity import BaseEntity
from utils.consts import SCREEN_SIZE
from utils.image import load_sprite_alpha

SPEED = 50

class Bullet(BaseEntity):
    def __init__(self, position: Vector2, angle: float, lin_velocity: float):
        super().__init__(
            sprite=load_sprite_alpha("bullet"),
            position=position,
            angle=angle,
        )
        
        self.velocity = self.orientation * (lin_velocity + SPEED)
        
    def tick(self, deltaTime: float):
        super().tick(deltaTime)

    def tick_bounds(self):
        if self.position.x > SCREEN_SIZE[0] or self.position.y > SCREEN_SIZE[1]:
            self.alive = False
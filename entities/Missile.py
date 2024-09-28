from pygame import Vector2
from entities.BaseEntity import BaseEntity
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

    
        
from pygame import Vector2
from entities.BaseEntity import BaseEntity
from utils.image import load_sprite_alpha

SPEED = 50

class Bullet(BaseEntity):
    def __init__(self, position: Vector2, rotation: float, linvelocity: float):
        super().__init__(position, load_sprite_alpha("bullet"))
        
        self.rotation = rotation
        self.velocity = self.orientation * (linvelocity + SPEED)
        
    def tick(self, deltaTime: float):
        super().tick(deltaTime)

    
        
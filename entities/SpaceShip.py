from pygame import Vector2
from entities.BaseEntity import BaseEntity
from utils.consts import SCREEN_SIZE
from utils.image import load_sprite_alpha

class SpaceShip(BaseEntity):
    ACC_MANEUVERABILITY = 100
    ROT_MANEUVERABILITY = 180
    DECELERATION = 0.1

    def __init__(self):
        self.rotate_input = 0
        self.acceleration_input = 0
        self.sprite_on = load_sprite_alpha("ship_on")
        self.sprite_off = load_sprite_alpha("ship_off")
        super().__init__(Vector2(SCREEN_SIZE)/2, None)

    @property
    def sprite(self):
        if self.acceleration_input > 0:
            return self.sprite_on
        else:
            return self.sprite_off

    def tick(self, deltaTime: float):
        self.velocity += self.orientation * (self.acceleration_input * self.ACC_MANEUVERABILITY * deltaTime)

        self.rotvelocity += self.rotate_input * self.ROT_MANEUVERABILITY * deltaTime
        self.rotvelocity *= 1 - self.DECELERATION
        
        super().tick(deltaTime)
        
from random import randint

from pygame import Vector2

from entities.BaseEntity import BaseEntity
from utils.consts import SCREEN_SIZE
from utils.image import load_sprite_alpha


class Asteroid(BaseEntity):
    def __init__(self, position: "Vector2", angle: float, lin_velocity: float, ang_velocity: float):
        super().__init__(
            sprite=load_sprite_alpha("asteroid"),
            position=position,
            angle=angle,
            ang_velocity=ang_velocity,
        )
        
        self.velocity = self.orientation * lin_velocity
        
    def tick(self, deltaTime: float):
        super().tick(deltaTime)

    @classmethod
    def random(cls):
        sprite = load_sprite_alpha("asteroid")
        position = Vector2()

        if randint(0,1) == 0:
            position = Vector2(randint(0, SCREEN_SIZE[0]), -sprite.get_height()/2)
        else:
            position = Vector2(-sprite.get_width()/2, randint(0, SCREEN_SIZE[1]))
        
        rotation = randint(0, 360)
        linvelocity = randint(100, 150)
        rotvelocity = randint(100, 150)

        return cls(position, rotation, linvelocity, rotvelocity)
        
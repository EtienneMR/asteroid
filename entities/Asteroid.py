from pygame import Vector2
from entities.BaseEntity import BaseEntity
from utils.image import load_sprite_alpha
from utils.consts import SCREEN_SIZE
from random import randint

class Asteroid(BaseEntity):
    def __init__(self, position: "Vector2", rotation: float, linvelocity: float, rotvelocity: float):
        super().__init__(position, load_sprite_alpha("asteroid"))
        
        self.destroyed = False
        self.rotation = rotation
        self.velocity = self.orientation * linvelocity
        self.rotvelocity = rotvelocity
        
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
        
from random import randint

from pygame import Vector2

from entities.BaseEntity import BaseEntity
from utils.assets import load_sprite_alpha
from utils.consts import SCREEN_SIZE


class Asteroid(BaseEntity):
    def __init__(
        self,
        position: "Vector2",
        angle: float,
        lin_velocity: float,
        ang_velocity: float,
        scale: float,
    ):
        super().__init__(
            sprite=load_sprite_alpha("asteroid"),
            position=position,
            angle=angle,
            ang_velocity=ang_velocity,
            scale=scale,
        )

        self.velocity = self.orientation * lin_velocity

    @property
    def breakable(self):
        return self.scale > 0.25

    def split(self):
        self.scale /= 2

        return Asteroid(
            self.position,
            self.angle + 180 + randint(-90, 90),
            self.velocity.magnitude() + randint(-10, 10),
            self.ang_velocity,
            self.scale,
        )

    @classmethod
    def random(cls, scale: float):
        sprite = load_sprite_alpha("asteroid")
        position = Vector2()

        if randint(0, 1) == 0:
            position = Vector2(randint(0, SCREEN_SIZE[0]), -sprite.get_height() / 2)
        else:
            position = Vector2(-sprite.get_width() / 2, randint(0, SCREEN_SIZE[1]))

        rotation = randint(0, 360)
        linvelocity = randint(100, 150)
        rotvelocity = randint(100, 150)

        return cls(position, rotation, linvelocity, rotvelocity, scale)

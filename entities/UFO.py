from random import randint

from pygame import Vector2

from entities.Asteroid import Asteroid
from entities.BaseEntity import BaseEntity
from utils.assets import load_sprite_alpha
from utils.consts import SCREEN_SIZE


class UFO(BaseEntity):
    SHOT_EVERY = 1

    def __init__(
        self,
        position: "Vector2",
        angle: float,
        lin_velocity: float,
        ang_velocity: float,
        scale: float,
    ):
        super().__init__(
            sprite=load_sprite_alpha("UFO"),
            position=position,
            angle=angle,
            ang_velocity=ang_velocity,
            scale=scale,
        )

        self.velocity = self.orientation * lin_velocity
        self.next_shot = self.SHOT_EVERY

    @property
    def breakable(self):
        return False

    def split(self):
        raise NotImplementedError("Can't split an UFO")

    @classmethod
    def random(cls, scale: float):
        sprite = load_sprite_alpha("UFO")
        position = Vector2()

        if randint(0, 1) == 0:
            position = Vector2(
                randint(0, SCREEN_SIZE[0]), -sprite.get_height() / 2 * scale
            )
        else:
            position = Vector2(
                -sprite.get_width() / 2 * scale, randint(0, SCREEN_SIZE[1])
            )

        rotation = randint(0, 360)
        linvelocity = randint(100, 150)
        rotvelocity = randint(100, 150)

        return cls(position, rotation, linvelocity, rotvelocity, scale)

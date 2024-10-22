from pygame import Vector2

from entities.BaseEntity import BaseEntity
from utils.assets import load_sprite_alpha
from utils.consts import SCREEN_SIZE

SPEED = 50


class Bullet(BaseEntity):
    def __init__(
        self, position: Vector2, angle: float, lin_velocity: float, friendly: bool
    ):
        super().__init__(
            sprite=load_sprite_alpha("bullet"),
            position=position,
            angle=angle,
        )

        self.friendly = friendly
        self.velocity = self.orientation * (lin_velocity + SPEED)

    def tick_bounds(self):
        x = self.position.x
        y = self.position.y

        if (
            x >= SCREEN_SIZE[0] + self.radius
            or x < -self.radius
            or y >= SCREEN_SIZE[1] + self.radius
            or y < -self.radius
        ):
            self.alive = False

    @property
    def breakable(self):
        return False

    def split(self):
        raise NotImplementedError("Can't split a bullet")

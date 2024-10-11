from pygame import Surface, Vector2, transform

from entities.BaseEntity import BaseEntity
from utils.assets import load_sound, load_sprite_alpha
from utils.consts import SCREEN_SIZE

GOD_TIME = 5.0

LIN_ACCELERATION = 100  # px/s²
ANG_ACCELERATION = 360  # deg/s²
ANG_FRICTION = 0.25  # /s
ANG_FRICTION_SCALE = 50  # s/px
SIZE = 40  # px
SIZE_RATIO = 65 / 81  # px/px

INIT_ANGLE = 90
INIT_VELOCITY = Vector2(0, -50)


class SpaceShip(BaseEntity):
    """
    Classe SpaceShip, représente un vaisseau contrôlable.
    Il n'y a qu'une seule instance de cette classe crée dans main.py et mutée directement dedans.
    Il est recréé en cas de mort.
    """

    def __init__(self):
        """
        Initialise le vaisseau.
        """
        self.rotate_input = 0
        self.acceleration_input = 0

        size = (SIZE, int(SIZE * SIZE_RATIO))

        self.sprite_on = transform.scale(load_sprite_alpha("ship_on"), size)
        self.sprite_off = transform.scale(load_sprite_alpha("ship_off"), size)

        self.god_time = GOD_TIME

        super().__init__(
            sprite=None,
            position=Vector2(
                SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] + self.sprite.get_height() / 2
            ),
            angle=INIT_ANGLE,
            velocity=INIT_VELOCITY,
        )

    @property
    def sprite(self):
        """
        Changement du sprite en fonction de l'action du joueur.
        """
        if self.acceleration_input > 0:
            return self.sprite_on
        else:
            return self.sprite_off

    def draw(self, surface: Surface):
        if int(self.god_time * 2) % 2 == 0:
            super().draw(surface)

    def tick(self, deltaTime: float):
        """
        Accélération et accélération angulaire.
        """
        self.velocity += self.orientation * (
            self.acceleration_input * LIN_ACCELERATION * deltaTime
        )

        self.ang_velocity += self.rotate_input * ANG_ACCELERATION * deltaTime
        self.ang_velocity *= 1 - ANG_FRICTION * deltaTime * (
            1 + abs(self.ang_velocity) / ANG_FRICTION_SCALE
        )

        self.god_time = max(self.god_time - deltaTime, 0.0)

        super().tick(deltaTime)

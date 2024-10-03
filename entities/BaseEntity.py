from typing import Optional

from pygame import Surface
from pygame.math import Vector2
from pygame.transform import rotozoom

from classes.IRenderable import IRenderable
from utils.consts import SCREEN_SIZE


class BaseEntity(IRenderable):
    """
    Classe BaseEntity, représente une entitée du jeu.
    N'a pas beaucoup d'utilité seule mais peut être héritée.
    """
    def __init__(self, sprite: Optional[Surface], position: Vector2 = Vector2(0,0), angle: float = 0, velocity: Vector2 = Vector2(0, 0), ang_velocity: float = 0):
        """
        Initialise la BaseEntity
        """
        self.position = Vector2(position)
        self.angle = angle
        self.velocity = Vector2(velocity)
        self.ang_velocity = ang_velocity
        self.alive = True

        if sprite is not None:
            self.sprite = sprite

    @property
    def radius(self) -> float:
        """
        Récupère le rayon du cercle autour de cet entitée.
        """
        return max(self.sprite.get_width(), self.sprite.get_height()) / 2
    
    @property
    def orientation(self):
        """
        Renvoie le Vector2 représentation la direction de cet entitée.
        """
        return Vector2.from_polar((1, -self.angle))

    def draw(self, surface: Surface):
        """
        Dessine cet entitée.
        """
        rotated_surface = rotozoom(self.sprite, self.angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def tick(self, deltaTime: float):
        """
        Met a jour la position et l'angle de cet entitée
        """
        self.position += self.velocity * deltaTime
        self.angle += self.ang_velocity * deltaTime

        self.tick_bounds()

    def tick_bounds(self):
        width = self.sprite.get_width()
        height = self.sprite.get_height()

        self.position.x = (self.position.x + width/2) % (SCREEN_SIZE[0] + width) - width/2
        self.position.y = (self.position.y + height/2) % (SCREEN_SIZE[1] + height) - height/2

    def collides_with(self, other_obj: "BaseEntity"):
        """
        Vérifie si cet entitée est en contact avec une autre entitée.
        """
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
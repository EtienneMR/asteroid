from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.transform import rotozoom

from utils.consts import SCREEN_SIZE

UP = Vector2(0, -1)

class BaseEntity:
    def __init__(self, position: Vector2, sprite: Surface):
        self.position = Vector2(position)
        self.rotation = 0
        self.velocity = Vector2(0, 0)
        self.rotvelocity = 0

        if sprite is not None:
            self.sprite = sprite

    @property
    def radius(self) -> float:
        return self.sprite.get_width() / 2
    
    @property
    def orientation(self):
        return Vector2.from_polar((1, -self.rotation))

    def draw(self, surface: Surface):
        rotated_surface = rotozoom(self.sprite, self.rotation, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def tick(self, deltaTime: float):
        self.position += self.velocity * deltaTime
        self.rotation += self.rotvelocity * deltaTime
        
        width = self.sprite.get_width()
        height = self.sprite.get_height()

        self.position.x = (self.position.x + width/2) % (SCREEN_SIZE[0] + width) - width/2
        self.position.y = (self.position.y + height/2) % (SCREEN_SIZE[1] + height) - height/2

    def collides_with(self, other_obj: "BaseEntity"):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
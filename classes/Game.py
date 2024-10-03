from typing import Any

import pygame

from classes.EntitiesList import EntitiesList
from classes.UserInterface import UserInterface
from entities.Asteroid import Asteroid
from entities.Missile import Bullet
from entities.SpaceShip import SpaceShip
from utils.consts import SCREEN_SIZE
from utils.image import load_sprite

GAME_CAPTION = "Asteroids"


class Game:
    """
    Classe Game, représente le jeu en cours.
    S'occupe de toute la logique tel que la gestion du vaisseau et des niveaux.
    """

    def __init__(self: "Game"):
        """
        Initialise le jeu et pygame.
        """
        pygame.init()
        pygame.display.set_caption(GAME_CAPTION)

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = load_sprite("space")
        self.clock = pygame.time.Clock()
        self.userInterface = UserInterface()
        self.spaceship = SpaceShip()
        self.asteroids: EntitiesList[Asteroid] = EntitiesList(None)
        self.bullets: EntitiesList[Bullet] = EntitiesList(None)
        self.entities: EntitiesList[Any] = EntitiesList(
            [self.spaceship, self.asteroids, self.bullets, self.userInterface]
        )
        self.space_down_last_frame = False

    @property
    def level(self):
        return self.userInterface.level

    @level.setter
    def level(self, level: int):
        self.userInterface.level = level

    def main_loop(self: "Game"):
        """
        Démarre le jeu.
        """
        while True:
            deltaTime = self.clock.tick(60) / 1000
            self._handle_input()
            self._process_game_logic(deltaTime)
            self._draw()

    def _handle_input(self: "Game"):
        """
        Gère les évènements émits par les utilisateurs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pressed_keys = pygame.key.get_pressed()

        accel = 0
        rot = 0

        if pressed_keys[pygame.K_UP]:
            accel += 1
        if pressed_keys[pygame.K_RIGHT]:
            rot -= 1
        if pressed_keys[pygame.K_LEFT]:
            rot += 1
        if pressed_keys[pygame.K_SPACE] and not self.space_down_last_frame:
            self.bullets.append(
                Bullet(
                    self.spaceship.position,
                    self.spaceship.angle,
                    self.spaceship.velocity.magnitude(),
                )
            )

        self.space_down_last_frame = pressed_keys[pygame.K_SPACE]

        self.spaceship.acceleration_input = accel
        self.spaceship.rotate_input = rot

    def _process_game_logic(self: "Game", deltaTime: float):
        """
        Fait avancer la logique du jeu, notamment les entitées utilisées et l'apparition d'asteroids.
        """
        self.entities.tick(deltaTime)

        if len(self.asteroids) == 0:
            self.level += 1
            for _ in range(self.level ** 2):
                self.asteroids.append(Asteroid.random())

    def _draw(self: "Game"):
        """
        Affiche le jeu ainsi que les entitées utilisées.
        """
        self.screen.blit(self.background, (0, 0))
        self.entities.draw(self.screen)
        pygame.display.flip()

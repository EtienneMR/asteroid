import pygame
from typing import Self
from EntitiesList import EntitiesList
from entities.SpaceShip import SpaceShip
from entities.Asteroid import Asteroid
from entities.Missile import Bullet
from utils.consts import SCREEN_SIZE
from utils.image import load_sprite

GAME_CAPTION = "Asteroids"

class Game:
    """
    Classe Game, représente le jeu en cours.
    S'occupe de toute la logique tel que la gestion du vaisseau et des niveaux.
    """
    def __init__(self: Self):
        """
        Initialise le jeu et pygame.
        """
        pygame.init()
        pygame.display.set_caption(GAME_CAPTION)

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = load_sprite("space")
        self.clock = pygame.time.Clock()
        self.spaceship = SpaceShip()
        self.asteroids: EntitiesList[Asteroid] = EntitiesList()
        self.bullets: EntitiesList[Bullet] = EntitiesList()
        self.level = 0

    def main_loop(self: Self):
        """
        Démarre le jeu.
        """
        while True:
            deltaTime = self.clock.tick(60) / 1000
            self._handle_input()
            self._process_game_logic(deltaTime)
            self._draw()

    def _handle_input(self: Self):
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
        
        self.spaceship.acceleration_input = accel
        self.spaceship.rotate_input = rot

    def _process_game_logic(self: Self, deltaTime: float):
        """
        Fait avancer la logique du jeu, notamment les entitées utilisées et l'apparition d'asteroids.
        """
        self.spaceship.tick(deltaTime)
        for asteroid in self.asteroids:
            asteroid.tick(deltaTime)

        if len(self.asteroids) == 0:
            for _ in range((self.level + 1)**2):
                self.asteroids.append(Asteroid.random())

    def _draw(self: Self):
        """
        Affiche le jeu ainsi que les entitées utilisées.
        """
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        pygame.display.flip()
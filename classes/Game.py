import os
from typing import Any, List

import pygame

from classes.EntitiesList import EntitiesList
from classes.UserInterface import UserInterface
from entities.Asteroid import Asteroid
from entities.Bullet import Bullet
from entities.Explosion import Explosion
from entities.SpaceShip import SpaceShip
from entities.UFO import UFO
from utils.assets import load_sound, load_sprite
from utils.consts import SCREEN_SIZE

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

        self.space_down_last_frame = False
        self.explosions: EntitiesList[Explosion] = EntitiesList(None)

        self.sound_laser = load_sound("laser.wav", 0.5)

        self.sound_acc = load_sound("acceleration.mp3")
        self.sound_state = False

        self.reset(False)

    def reset(self: "Game", isrestart: bool):
        ast: Any = None
        sp: Any = None
        ufos: Any = None
        if isrestart:
            ast = self.asteroids
            sp = self.spaceship
            ufos = self.UFOs

        self.userInterface = UserInterface()
        self.spaceship: SpaceShip = SpaceShip()
        self.spaceships: EntitiesList[SpaceShip] = EntitiesList([self.spaceship])
        self.asteroids: EntitiesList[Asteroid] = EntitiesList(None)
        self.bullets: EntitiesList[Bullet] = EntitiesList(None)
        self.UFOs: EntitiesList[UFO] = EntitiesList(None)
        self.entities: EntitiesList[Any] = EntitiesList(
            [
                self.bullets,
                self.spaceships,
                self.asteroids,
                self.UFOs,
                self.explosions,
                self.userInterface,
            ]
        )

        if isrestart:
            for asteroid in ast:
                self.explosions.append(Explosion(asteroid.position))
            for ufo in ufos:
                self.explosions.append(Explosion(ufo.position))
            if sp.alive:
                self.explosions.append(Explosion(sp.position))

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
            self.handle_input()
            self.tick(deltaTime)
            self.draw(self.screen)

    def handle_input(self: "Game"):
        """
        Gère les évènements émits par les utilisateurs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pressed_keys = pygame.key.get_pressed()

        accel = 0
        rot = 0

        if pressed_keys[pygame.K_BACKSPACE] and self.spaceship.god_time == 0:
            return self.reset(True)
        if pressed_keys[pygame.K_s] and self.userInterface.gameover:
            self.save_score()
        if pressed_keys[pygame.K_UP]:
            accel += 1
        if pressed_keys[pygame.K_RIGHT]:
            rot -= 1
        if pressed_keys[pygame.K_LEFT]:
            rot += 1
        if (
            pressed_keys[pygame.K_SPACE]
            and not self.space_down_last_frame
            and self.spaceship.alive
        ):
            self.sound_laser.play()
            self.bullets.append(
                Bullet(
                    self.spaceship.position,
                    self.spaceship.angle,
                    self.spaceship.velocity.magnitude(),
                    True,
                )
            )

        self.space_down_last_frame = pressed_keys[pygame.K_SPACE]

        self.spaceship.acceleration_input = accel
        self.spaceship.rotate_input = rot

        should_play_sound = accel > 0
        if self.sound_state != should_play_sound:
            if should_play_sound > 0:
                self.sound_acc.play()
            else:
                self.sound_acc.fadeout(1000)
            self.sound_state = should_play_sound

    def save_score(self: "Game"):
        """
        Sauvegarde le score du joueur dans le fichier Scores.txt en ne conservant que les 10 meilleurs scores.
        """
        username = input("Entrez votre nom d'utilisateur : ")

        with open("Scores.txt", "w+") as file:
            lines = file.readlines()
            lines.append(f"{username} : {self.userInterface.score}\n")
            lines.sort(key=lambda l: int(l.split(" : ")[1]), reverse=True)
            while len(lines) > 10:
                lines.pop()
            file.seek(0)
            file.writelines(lines)
            file.truncate()

    def tick(self: "Game", deltaTime: float):
        """
        Fait avancer la logique du jeu, notamment les entitées utilisées et l'apparition d'asteroids.
        """
        self.entities.tick(deltaTime)

        if (
            len(self.asteroids) == 0
            and len(self.UFOs) == 0
            and self.spaceship.god_time == 0
        ):
            self.level += 1
            for _ in range(self.level):
                self.asteroids.append(Asteroid.random(1.0))
            for _ in range((self.level - 1) ** 2):
                self.asteroids.append(Asteroid.random(0.5))
            for asteroid in self.asteroids:
                asteroid.velocity += pygame.Vector2(self.level, self.level)
            if self.level % 2 == 0:
                for i in range(self.level // 2):
                    self.UFOs.append(UFO.random(i + 1))
            if self.level % 3 == 0:
                self.asteroids.append(Asteroid.random(4.0))

        for ufo in self.UFOs:
            ufo.next_shot -= deltaTime
            if ufo.next_shot < 0:
                ufo.next_shot += ufo.SHOT_EVERY
                self.bullets.append(
                    Bullet(
                        ufo.position,
                        ufo.angle,
                        ufo.velocity.magnitude(),
                        False,
                    )
                )

        enemyBullets = filter(lambda b: not b.friendly, self.bullets)

        collideables: List[Asteroid | UFO | Bullet] = []
        collideables.extend(self.asteroids)
        collideables.extend(self.UFOs)
        collideables.extend(enemyBullets)

        for collideable in collideables:
            if (
                self.spaceship.god_time == 0.0
                and self.spaceship.alive
                and collideable.collides_with(self.spaceship)
            ):
                self.explosions.append(Explosion(self.spaceship.position))
                self.spaceship.alive = False
                if self.userInterface.lives <= 0:
                    self.userInterface.gameover = True
                else:
                    self.spaceship = SpaceShip()
                    self.spaceships.append(self.spaceship)
                    self.userInterface.lives -= 1

            for bullet in self.bullets:
                if (
                    bullet.friendly
                    and bullet.alive
                    and collideable.collides_with(bullet)
                ):
                    self.explosions.append(Explosion(collideable.position))
                    bullet.alive = False
                    self.userInterface.score += int(100 * collideable.scale)
                    if collideable.breakable:
                        self.asteroids.append(collideable.split())
                    else:
                        collideable.alive = False

    def draw(self: "Game", surface: pygame.Surface):
        """
        Affiche le jeu ainsi que les entitées utilisées.
        """
        self.screen.blit(self.background, (0, 0))
        self.entities.draw(surface)
        pygame.display.flip()

from pygame import Surface
from entities.BaseEntity import BaseEntity
from typing import Generic, TypeVar

EntityType = TypeVar("EntityType", bound=BaseEntity)

class EntitiesList(Generic[EntityType]):
    """
    Classe EntitiesList, représente une liste de BaseEntity.
    """
    def __init__(self) -> None:
        """
        Initialise la liste d'entitées.
        """
        self._entities: list[EntityType] = []

    def __iter__(self):
        """
        Permet l'itération.
        """
        return iter(self._entities)
    
    def __len__(self):
        """
        Permet l'accès a la longueur.
        """
        return len(self._entities)

    def append(self, entity: EntityType):
        """
        Ajoute une entitée a la liste.
        """
        self._entities.append(entity)

    def draw(self, surface: Surface):
        """
        Dessine toutes les entitées de la liste.
        """
        for entity in self._entities:
            entity.draw(surface)

    def tick(self, deltaTime: float):
        """
        Met a jour toutes les entitées de la liste puis ne garde que les entitées en vie.
        """
        filtered = []
        for entity in self._entities:
            entity.tick(deltaTime)
            if entity.alive:
                filtered.append(entity)
        self._entities = filtered

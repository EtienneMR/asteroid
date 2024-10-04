from typing import Generic, List, Optional, TypeVar

from pygame import Surface

from classes.IRenderable import IRenderable

EntityType = TypeVar("EntityType", bound=IRenderable)

class EntitiesList(Generic[EntityType]):
    """
    Classe EntitiesList, représente une liste de BaseEntity.
    """
    def __init__(self, list: Optional[List[EntityType]]) -> None:
        """
        Initialise la liste d'entitées.
        """
        self._entities: List[EntityType] = list or []

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
    
    @property
    def alive(self):
        return True

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

        for entity in self._entities:
            entity.tick(deltaTime)
        
        self._entities = list(filter(lambda e: e.alive, self._entities))
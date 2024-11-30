from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

class Storable(ABC):
    @abstractmethod
    def get_id(self):
        raise NotImplementedError

@dataclass
class DisgaeaCharacter(Storable):
    name: str
    equipment: list[str]

    def __init__(self, name: str, equipment: list[str]):
        valid_equipment = {
            "sword",
            "spear",
            "axe",
            "bow_arrow",
            "gun",
            "fist",
            "staff",
            "monster_phy",
            "monster_int",
            "armor",
            "belt",
            "shoes",
            "glasses",
            "orb",
            "muscle",
            "emblem",
            "special"
        }
        invalid_equipments_specified = set(equipment).difference(valid_equipment)
        if invalid_equipments_specified:
            raise ValueError(f"invalid equipment specified: {str.join(', ', invalid_equipments_specified)}")
        
        self.name = name
        self.equipment = equipment

    def get_id(self):
        return self.name


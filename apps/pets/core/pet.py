from .actions.ball import Ball
from .base import BasePetMaster
from .menu import PetMenu


class BallPet(BasePetMaster):
    def __init__(self):
        super().__init__()
        self.action = Ball(self)
        if not self.menu:
            self.menu = PetMenu(self)




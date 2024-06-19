from .actions.ball import Ball
from .actions.biu import Biu
from .actions.cat import Cats
from .actions.lxh import Lxh
from .base import BasePetMaster
from .menu import PetMenu


class CatPet(BasePetMaster):
    """
    默认配置
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.action = Cats(self)
        if not self.menu:
            self.menu = PetMenu(self)


class BiuPet(BasePetMaster):
    def __init__(self):
        super().__init__()
        self.action = Biu(self)
        if not self.menu:
            self.menu = PetMenu(self)


class LxhPet(BasePetMaster):
    def __init__(self):
        super().__init__()
        self.action = Lxh(self)
        if not self.menu:
            self.menu = PetMenu(self)

class BallPet(BasePetMaster):
    def __init__(self):
        super().__init__()
        self.action = Ball(self)
        if not self.menu:
            self.menu = PetMenu(self)




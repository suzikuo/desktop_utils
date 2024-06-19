from apps.app import BaseApp
from apps.pets.core.pet import BallPet, BiuPet, CatPet, LxhPet
from kernel.events import StopEvents
from log import MyLogger


class PetsApp(BaseApp):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "Pets"

    def run(self):
        try:
            default = "ball"
            pet_conf = {"cat": CatPet, "biu": BiuPet, "lxh": LxhPet,"ball":BallPet}
            self.pet = pet_conf[default]()
            StopEvents().add("Pet", self.pet.quit)
            self.pet.run()
        except Exception as e:
            MyLogger.error("Pet APP:start service error:{}".format(e))
            raise e
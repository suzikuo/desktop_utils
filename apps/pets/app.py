from apps.app import BaseApp
from apps.pets.core.pet import BallPet
from kernel.events import StopEvents
from log import MyLogger


class PetsApp(BaseApp):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "Pets"

    def run(self):
        try:
            self.pet = BallPet()
            StopEvents().add("Pet", self.pet.quit)
            self.pet.run()
        except Exception as e:
            MyLogger.error("Pet APP:start service error:{}".format(e))
            raise e
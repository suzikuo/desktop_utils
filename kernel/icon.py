import threading

import pystray
from PIL import Image
from pystray import MenuItem as item

from kernel.settings import config
from singleton import singleton

from .events import StopEvents


@singleton
class IconMenu:
    def __init__(self) -> None:
        self.icon = None

        self._stopping = False

    def run(self):
        threading.Thread(target=self.system_action).start()

    def system_action(self):
        menu = (item("Exit", self.exit_app),)
        image = Image.open(config.icon.img)
        # 加载图标
        self.icon = pystray.Icon("MyBall", image, "MyBall", menu)
        self.icon.run()

    def exit_app(self, *args, **kwargs):
        if self._stopping:
            return
        self._stopping = True
        stop_events = StopEvents()
        for name, event in stop_events.l.items():
            stop_events.stop(name, event)

        self.icon.stop()
        self._stopping = False

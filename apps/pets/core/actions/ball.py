import os

from kernel.settings import IMG_DIR, config

from ..base import BaseAction
from ..log import PetLogger


class Ball(BaseAction):
    """
    球
    """

    def __init__(self, main) -> None:
        super().__init__(main)

        self.init_images()

        self.top_level = None

        PetLogger.info("Pet APP:Init action success!")

        self.timer = (
            10 if not config.pet.ball.default_timer else config.pet.ball.default_timer
        )

        self.running = False

    def init_text_label(self):
        pass

    def init_images(self):
        from tkinter import PhotoImage

        self.image = PhotoImage(file=os.path.join(IMG_DIR, "ball\\ball_new.png"))

        self.photo_images = [self.image]

        self.lens = len(self.photo_images)

    def update(self, i, curr_animation):
        if i == self.lens:
            i = 0
        self.action_label.configure(image=self.photo_images[i])
        i += 1
        if self.running:
            self.main.root.after(self.timer, self.update, i, curr_animation)

    def onLeftDrag(self, event):
        x = self.main.root.winfo_x() + event.x - self.offset_x
        y = self.main.root.winfo_y() + event.y - self.offset_y
        self.curr_width = x
        self.curr_height = y
        self.geometry()

    def init_position(self):
        super().init_position()
        self.geometry()

    def onLeftClick(self, event):
        super().onLeftClick(event)
        self.offset_x = event.x
        self.offset_y = event.y

    def onLeftPress(self, event):
        self.timer = config.pet.ball.onLeftPress_timer
        self.offset_x = event.x
        self.offset_y = event.y

    def onLeftRelease(self, event):
        self.timer = config.pet.ball.default_timer

    def quit(self):
        # sys.exit(0)
        return super().quit()

    def onLeftDoubleClick(self, event):
        pass

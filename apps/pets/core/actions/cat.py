import os
import random
import tkinter

from kernel.settings import IMG_DIR, config

from ..base import BaseAction
from ..hitokoto import Hitokoto
from ..log import PetLogger


class Cats(BaseAction):
    """
    猫
    """

    def __init__(self, main) -> None:
        super().__init__(main)

        self.move_speed = 6

        self.size = ""

        self.init_animation()

        # 添加名言语句
        self.hitokoto = Hitokoto(self.text_label)

        PetLogger.info("Pet APP:Init action success!")

    def init_animation(self):
        self.animation_config = dict(
            idle=[os.path.join(IMG_DIR, f"cat\\idle{self.size}.gif"), 5],
            idle_to_sleep=[
                os.path.join(IMG_DIR, f"cat\\idle-to-sleep{self.size}.gif"),
                7,
            ],
            sleep=[os.path.join(IMG_DIR, f"cat\\sleep{self.size}.gif"), 3],
            sleep_to_idle=[
                os.path.join(IMG_DIR, f"cat\\sleep-to-idle{self.size}.gif"),
                7,
            ],
            walk_left=[os.path.join(IMG_DIR, f"cat\\walk-left{self.size}.gif"), 8],
            walk_right=[os.path.join(IMG_DIR, f"cat\\walk-right{self.size}.gif"), 8],
        )
        self.animation = {
            key: [
                tkinter.PhotoImage(file=config[0], format=f"gif -index {i}")
                for i in range(config[1])
            ]
            for key, config in self.animation_config.items()
        }

    def update(self, i, curr_animation):
        if curr_animation is None:
            curr_animation = "idle"
        self.main.root.attributes("-topmost", True)
        animation_arr = self.animation[curr_animation]
        self.action_label.configure(image=animation_arr[i])
        # move the pet if needed
        if curr_animation in ("walk_left", "walk_right"):
            self.move_window(curr_animation)

        i += 1
        if i == len(animation_arr):
            next_animation = self.getNextAnimation(curr_animation)
            self.main.root.after(self.main.delay, self.update, 0, next_animation)
        else:
            self.main.root.after(self.main.delay, self.update, i, curr_animation)

    def move_window(self, curr_animation):
        if not config.pet.can_move:
            return
        if curr_animation == "walk_left":
            if self.curr_width > self.min_width:
                self.curr_width -= self.move_speed

        elif curr_animation == "walk_right":
            if self.curr_width < self.max_width:
                self.curr_width += self.move_speed

        self.geometry()

    def getNextAnimation(self, curr_animation):
        if curr_animation == "idle":
            return random.choice(["idle", "idle_to_sleep", "walk_left", "walk_right"])
        elif curr_animation == "idle_to_sleep":
            return "sleep"
        elif curr_animation == "sleep":
            return random.choice(["sleep", "sleep_to_idle"])
        elif curr_animation == "sleep_to_idle":
            return "idle"
        elif curr_animation == "walk_left":
            return random.choice(["idle", "walk_left", "walk_right"])
        elif curr_animation == "walk_right":
            return random.choice(["idle", "walk_left", "walk_right"])

    def onLeftDrag(self, event):
        # 更新窗口位置为鼠标移动后的位置
        x = self.main.root.winfo_pointerx() - self.offset_x
        y = self.main.root.winfo_pointery() - self.offset_y
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

    def quit(self):
        self.hitokoto.quit()
        return super().quit()

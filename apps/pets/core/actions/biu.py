import os
import random
import tkinter

from PIL import Image, ImageSequence, ImageTk

from kernel.settings import IMG_DIR, config

from ..base import BaseAction
from ..menu import BiuPetMenu
from .animated_gif import AnimatedGIF

BASE_DIR = os.path.join(IMG_DIR, "biu")


class Biu(BaseAction):
    """
    biu
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        self.main = main
        self.root = self.main.root
        self.after_id = None

        self.size = 0.5

        self.init_position()

        self.delay = 100

        self.move_speed = 0.6

        # 创建Canvas对象
        self.canvas = tkinter.Canvas(self.root, bg="black")
        self.canvas.place(x=50, y=50)

        self.init_animation()

        # 当前图片
        self.curr_animation = self.animation["static"]["biu0"]
        self.type = "static"

        # 加载gif
        self.gif_player = AnimatedGIF(
            self.canvas, self.animation["static"]["biu0"], delay=100
        )
        self.gif_player.pack()
        self.popup = None

        self.main.menu = BiuPetMenu(self.main, self)

        self.top_level = None

    def update(self, i, curr_animation, type=None):
        i += 1
        self.curr_animation = curr_animation
        self.type = type
        if self.gif_player.is_start:
            if type in ["left_move", "right_move"]:
                self.move_window(curr_animation, type)

            self.after_id = self.main.root.after(
                10, self.update, i, curr_animation, type
            )
            return

        type, next_animation = self.getNextAnimation(curr_animation, type)
        self.gif_player.update_frames(self.animation[type][next_animation])

        self.after_id = self.main.root.after(10, self.update, i, next_animation, type)

    def getNextAnimation(self, curr_animation, type=None):
        if type == "left_click_keep":
            return "left_click_keep", curr_animation
        if random.randint(1, 1000) > 300:
            return "static", "biu0"

        type = random.choices(
            ["static", "left_move", "right_move"], weights=[8, 1, 1], k=1
        )[0]
        return type, random.choice(list(self.animation[type].keys()))

    def move_window(self, curr_animation, type):
        if not config.pet.can_move:
            return
        if type == "left_move":
            if self.curr_width > self.min_width:
                self.curr_width -= self.move_speed
        if type == "right_move":
            if self.curr_width < self.max_width:
                self.curr_width += self.move_speed
        self.geometry()
        if self.popup:
            self.popup.geometry(self.curr_width, self.curr_height)

    def init_action_label(self):
        return

    def onLeftDrag(self, event):
        # 更新窗口位置为鼠标移动后的位置
        x = event.x - self.offset_x
        y = event.y - self.offset_y
        self.curr_width += x
        self.curr_height += y
        self.geometry()

    def init_position(self):
        super().init_position()
        self.geometry()

    def onLeftClick(self, event):
        super().onLeftClick(event)
        self.offset_x = event.x
        self.offset_y = event.y
        if self.type in ["left_move", "right_move"]:
            return
        self.update_frames("left_click")

    def onLeftDoubleClick(self, event):
        pass

    def onLeftPress(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        if self.type in ["left_move", "right_move"]:
            return
        self.update_frames("left_click_keep")

    def onLeftRelease(self, event):
        if self.type in ["left_move", "right_move"]:
            return
        self.update_frames("static", "biu0")

    def update_frames(self, type, next_animation=None):
        # 取消先前的动画定时器
        if self.after_id:
            self.main.root.after_cancel(self.after_id)
            self.after_id = None
        if not next_animation:
            next_animation = random.choice(list(self.animation[type].keys()))
        self.gif_player.update_frames(self.animation[type][next_animation])
        self.main.root.after(10, self.update, 0, next_animation, type)

    def eat_foot(self, *args, **kwargs):
        self.update_frames("eat")

    def play(self, *args, **kwargs):
        self.update_frames("play")

    def close(self, *args, **kwargs):
        if self.hitokoto:
            self.hitokoto.set_text("bye bye ~~~")
        self.update_frames("bye")

    def init_animation(self):
        conf = {
            "static": [
                ["biu0.gif", 4],
                "biu2.gif",
                "biu5.gif",
                ["biu8.gif", 4],
                # "biu10.gif",
                # "biu12.gif",
                # "biu13.gif",
            ],
            "left_click": [
                "biu4.gif",
            ],
            "left_click_keep": [
                "biu6.gif",
                "biu7.gif",
            ],
            "right_click": [],
            "left_move": [
                "biuw0.gif",
            ],
            "right_move": [
                "biuw1.gif",
            ],
            "eat": [
                "biu1.gif",
                "biu3.gif",
                "biu11.gif",
            ],
            "play": [
                "biu9.gif",
            ],
            "bye": [
                "biu99.gif",
            ],
        }

        self.animation = {}

        for type, gif_list in conf.items():
            if type not in self.animation:
                self.animation[type] = {}

            for gif in gif_list:
                n = gif[1] if isinstance(gif, list) else 1
                gif = gif[0] if isinstance(gif, list) else gif
                self.animation[type][gif.replace(".gif", "").replace("biu/", "")] = [
                    (
                        ImageTk.PhotoImage(
                            i.convert("RGBA").resize(
                                (int(i.width * self.size), int(i.height * self.size))
                            )
                        ),
                        i.info["duration"],
                    )
                    for i in ImageSequence.Iterator(
                        Image.open(os.path.join(BASE_DIR, gif))
                    )
                ] * n

    def quit(self):
        if self.hitokoto:
            self.hitokoto.quit()
        return super().quit()

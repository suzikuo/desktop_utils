import os
import random
import tkinter

from PIL import Image, ImageSequence, ImageTk

from kernel.settings import IMG_DIR, config

from ..base import BaseAction
from ..menu import BiuPetMenu
from .animated_gif import AnimatedGIF

BASE_DIR = os.path.join(IMG_DIR, "lxh")


class Lxh(BaseAction):
    """
    Lxh
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        self.main = main
        self.root = self.main.root
        self.after_ids = set()

        self.size = 0.5

        self.init_position()

        self.delay = 100

        self.move_speed = 0.6

        # 创建Canvas对象
        self.canvas = tkinter.Canvas(self.root, bg="black")
        self.canvas.place(x=50, y=50)
        self.canvas.bind("<Enter>", self.on_mouse_enter)
        self.canvas.bind("<Leave>", self.on_mouse_leave)

        self.init_animation()

        # 当前图片
        self.curr_animation = None
        self.type = None

        # 加载gif
        self.gif_player = AnimatedGIF(
            self.canvas, self.animation["static"]["罗小黑0"], delay=100
        )
        self.gif_player.pack()

        self.main.menu = BiuPetMenu(self.main, self)

    def update(self, i, curr_animation, type=None):
        i += 1
        self.curr_animation = curr_animation
        self.type = type

        if self.gif_player.is_start:
            if type in ["left_move", "right_move"]:
                self.move_window(curr_animation, type)

            after_id = self.main.root.after(10, self.update, i, curr_animation, type)
            self.after_ids.add(after_id)
            return

        type, next_animation = self.getNextAnimation(curr_animation, type)
        self.gif_player.update_frames(self.animation[type][next_animation])

        after_id = self.main.root.after(100, self.update, i, next_animation, type)
        self.after_ids.add(after_id)

    def getNextAnimation(self, curr_animation, type=None):
        if random.randint(1, 1000) > 300:
            return "static", "罗小黑0"

        if type == "left_click_keep":
            return "left_click_keep", curr_animation

        if type == "mouse_enter":
            return "mouse_enter", curr_animation

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

    def init_action_label(self):
        return

    def on_mouse_enter(self, event):
        if self.type not in ["static"]:
            return
        # self.update_frames("mouse_enter")

    def on_mouse_leave(self, event):
        pass

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
        if self.type not in ["static", "mouse_enter"]:
            return
        self.update_frames("left_click")

    def onLeftPress(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        if self.type not in ["static"]:
            return
        self.update_frames("left_click_keep")

    def onLeftRelease(self, event):
        if self.type not in ["static"]:
            return
        self.update_frames("static", "罗小黑8")

    def update_frames(self, type, next_animation=None):
        # 取消先前的动画定时器
        if self.after_ids:
            for id in self.after_ids:
                self.main.root.after_cancel(id)
            self.after_id = set()
        if not next_animation:
            next_animation = random.choice(list(self.animation[type].keys()))
        self.gif_player.update_frames(self.animation[type][next_animation])
        self.main.root.after(10, self.update, 0, next_animation, type)

    def eat_foot(self, *args, **kwargs):
        self.update_frames("eat")

    def play(self, *args, **kwargs):
        self.update_frames("play")

    def close(self, *args, **kwargs):
        self.hitokoto.set_text("bye bye ~~~")
        self.update_frames("bye")

    def init_animation(self):
        conf = {
            "static": [
                ["罗小黑0.gif", 4],
                "罗小黑1.gif",
                ["罗小黑5.gif", 4],
                ["罗小黑8.gif", 4],
                ["罗小黑4.gif", 4],
                ["罗小黑11.gif", 4],
            ],
            "left_click": [
                ["罗小黑10.gif", 4],
            ],
            "left_click_keep": [
                ["罗小黑4.gif", 4],
                "罗小黑2.gif",
                ["罗小黑6.gif", 2],
            ],
            "right_click": [],
            "left_move": [
                ["罗小黑7.gif", 4],
                ["罗小黑w0.gif", 4],
            ],
            "right_move": [
                ["罗小黑w1.gif", 4],
            ],
            "eat": [
                ["罗小黑9.gif", 4],
            ],
            "play": [
                "罗小黑2.gif",
                ["罗小黑6.gif", 6],
            ],
            "bye": [
                ["罗小黑99.gif", 2],
            ],
            "mouse_enter": [
                "罗小黑2.gif",
                ["罗小黑6.gif", 2],
            ],
        }

        self.animation = {}

        for type, gif_list in conf.items():
            if type not in self.animation:
                self.animation[type] = {}

            for gif in gif_list:
                n = gif[1] if isinstance(gif, list) else 1
                gif = gif[0] if isinstance(gif, list) else gif
                self.animation[type][gif.replace(".gif", "").replace("lxh/", "")] = [
                    (
                        ImageTk.PhotoImage(
                            i.resize(
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

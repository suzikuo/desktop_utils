import datetime
import os
import time
import tkinter


from kernel.settings import BASE_DIR,IMG_DIR, config

from .hitokoto import Hitokoto


class BasePetMaster:
    """
    宠物的总类
    """
    def __init__(self):
        self.root = tkinter.Tk()  # create window
        self.root.withdraw()
        self.delay = 200  # delay in ms

        # window configuration
        self.root.overrideredirect(True)  # remove UI
        self.root.wm_attributes("-transparent", "black")

        self.root.attributes("-topmost", True)  # put window on top
        self.root.bind("<ButtonRelease>", self.onLeftRelease)
        self.root.bind("<ButtonPress>", self.onLeftPress)
        # self.root.bind("<Button-1>", self.onLeftClick)
        self.root.bind("<B1-Motion>", self.onLeftDrag)
        self.root.bind("<Button-3>", self.onRightClick)
        self.root.bind("<Double-Button-1>", self._onLeftDoubleClick)

        # 创建宠物
        self.action: BaseAction = None

        # 创建右键菜单
        self.menu: BaseMenu = None

        self.pressed = False

        # 双击的间隔
        self.double_press_time = time.time()  # 记录按下的时间

    def update(self, i, curr_animation):
        self.action.update(i, curr_animation)

    def _onLeftDoubleClick(self, event):
        if time.time() - self.double_press_time <= 1:
            self.onLeftClick(event)
        else:
            self.onLeftDoubleClick(event)
        self.double_press_time = time.time()  # 记录按下的时间

    def onLeftDoubleClick(self, event):
        self.action.onLeftDoubleClick(event)

    def onLeftDrag(self, event):
        """
        拖拽事件
        """
        self.action.onLeftDrag(event)

    def onLeftPress(self, event):
        """
        左键按下事件
        """
        self.pressed = True
        self.press_time = time.time()  # 记录按下的时间
        self.root.after(
            200, self.check_left_long_click, event
        )  # 在100ms后检查是否是长按

    def onLeftRelease(self, event):
        """
        左键抬起事件
        """
        if (
            event.num == 1 and self.pressed and (time.time() - self.press_time) >= 0.2
        ):  # 检查左键是否释放
            self.pressed = False
            self.action.onLeftRelease(event)
        self.pressed = False
        self.press_time = None

    def onLeftClick(self, event):
        """
        点击左键事件
        """
        self.action.onLeftClick(event)
        self.menu.onLeftClick(event)

    def onRightClick(self, event):
        """
        点击右键事件
        """
        self.action.onRightClick(event)
        self.menu.onRightClick(event)

    def check_left_long_click(self, event):
        """
        检查左键是否为长按
        """
        if (
            self.pressed and (time.time() - self.press_time) >= 0.2
        ):  # 如果按键仍然按下并且持续时间大于0.3秒
            self.long_pressed = True
            self.action.onLeftPress(event)
        else:
            self.long_pressed = False
            self.onLeftClick(event)

    def run(self):
        self.root.after(self.delay, self.update, 0, None)  # start on idle
        self.root.update_idletasks()
        self.root.deiconify()
        self.root.mainloop()


    def quit(self, *args, **kwargs):
        
        if self.action:
            self.action.quit()

        if self.menu:
            self.action.quit()
        # self.root.destroy()
        self.root.quit()


class BaseAction:
    def __init__(self, main: BasePetMaster) -> None:
        self.main = main
        self.root = self.main.root
        # 设置窗口大小
        self.window_width = config.pet.window_width
        self.window_height = config.pet.window_height

        self.init_background()

        self.init_position()

        self.init_text_label()

        self.init_time_label()

        self.init_action_label()

        self.animation = dict()

    def init_background(self):
        # 设置透明背景
        self.background = tkinter.Label(self.root, bd=0, bg="black")
        self.background.place(x=0, y=0)  # 设置 action_label 的初始位置
        self.background.configure(
            image=tkinter.PhotoImage(
                file=os.path.join(IMG_DIR, "transparent_image.png"),
                width=self.window_width,  # 设置宽度为250
                height=self.window_height,  # 设置高度为250
            )
        )

    def init_action_label(self):
        # 宠物窗口
        self.action_label = tkinter.Label(self.root, bd=0, bg="black")
        self.action_label.place(x=0, y=60)  # 设置 action_label 的初始位置

    def init_text_label(self):
        self.hitokoto = None
        # 创建文本框
        self.text_label = tkinter.Label(
            self.root,
            text="嗨嗨嗨~",
            bd=0,
            bg="black",
            fg=config.pet.text_label.fg,  # 修改为黑色文本
            font=(config.pet.font, config.pet.font_size),
            highlightthickness=0,  # 去除边框
        )
        self.text_label.place(x=0, y=30)  # 设置文本框的初始位置

        if config.pet.start_hitokoto:
            self.hitokoto = Hitokoto(self.text_label)
            self.hitokoto.start()
        else:
            self.hitokoto = None

    def init_time_label(self):
        if config.pet.show_time:
            # 创建时间框
            self.time_label = TimeLabel(
                self.root,
                text="2024年5月24日10:00:50",
                bd=0,
                bg="black",
                fg="grey",  # 修改为黑色文本
                font=("", 10),
                highlightthickness=0,  # 去除边框
            )
            self.time_label.place(x=0, y=0)  # 设置文本框的初始位置
            self.time_label.start()

    def init_position(self):
        self.offset_x = 0
        self.offset_y = 0
        self.pixels_from_right = 400  # change to move the pet's starting position
        self.pixels_from_bottom = 400  # change to move the pet's starting position
        screen_width = self.root.winfo_screenwidth()  # width of the entire screen
        screen_height = self.root.winfo_screenheight()  # height of the entire screen
        self.min_width = 10  # do not let the pet move beyond this point
        self.max_width = screen_width - 220  # do not let the pet move beyond this point

        # change starting properties of the window
        self.curr_width = screen_width - self.pixels_from_right
        self.curr_height = screen_height - self.pixels_from_bottom

    def onLeftClick(self, event):
        pass

    def onRightClick(self, event):
        pass

    def onLeftDrag(self, event):
        pass

    def onLeftPress(self, event):
        pass

    def onLeftRelease(self, event):
        pass

    def onLeftDoubleClick(self, event):
        pass

    def update(self, i, curr_animation):
        pass

    def geometry(self):
        """
        更新位置
        """
        self.main.root.geometry(
            "%dx%d+%d+%d"
            % (self.window_width, self.window_height, self.curr_width, self.curr_height)
        )

    def quit(self):
        pass
    
    def change_image(self):
        """
        换肤
        """
        pass


class BaseMenu(tkinter.Menu):
    """
    右键菜单
    """
    def __init__(self, main: BasePetMaster, *args, tearoff=False, **kwargs) -> None:
        super().__init__(main.root, *args, tearoff=tearoff, **kwargs)
        self.main = main
        self.root = self.main.root
        self.active = False

    def onLeftClick(self, event):
        pass

    def onRightClick(self, event):
        pass

    def onLeftPress(self, event):
        pass

    def quit(self):
        pass


class TimeLabel(tkinter.Label):
    """
    时间类
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def start(self):
        self.update_time()

    def update_time(self):
        t = datetime.datetime.now().strftime("%H:%M:%S %m/%d")
        self.config(text=t)

        self.after(500, self.update_time)

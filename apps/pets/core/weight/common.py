import re
from tkinter import Frame, X, TOP, BOTTOM, Y, LEFT, RIGHT, Label,Button
from tkinter.font import nametofont, Font
from tkinter.scrolledtext import ScrolledText


class SimpleMarkdownText(ScrolledText):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = Font(**default_font.configure())
        italic_font = Font(**default_font.configure())
        self.vbar.pack_forget()
        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")

        # self.config(yscrollbar=False, xscrollbar=False)

        # Small subset of markdown. Just enough to make text look nice.
        self.tag_configure("**", font=bold_font)
        self.tag_configure("*", font=italic_font)
        self.tag_configure("_", font=italic_font)
        self.tag_chars = "*_"
        self.tag_char_re = re.compile(r"[*_]")

        max_heading = 3
        for i in range(1, max_heading + 1):
            header_font = Font(**default_font.configure())
            header_font.configure(size=int(default_size * i + 3), weight="bold")
            self.tag_configure(
                "#" * (max_heading - i), font=header_font, spacing3=default_size
            )

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)
        lmargin2 = em + default_font.measure("1. ")
        self.tag_configure("numbered", lmargin1=em, lmargin2=lmargin2)

        self.numbered_index = 1

    def hide_vertical_scrollbar(self):
        bg_color = self.cget("background") or "white"  # 使用控件的背景颜色或默认白色
        self.vbar.config(bg=bg_color, activebackground=bg_color)

    def insert_bullet(self, position, text):
        self.insert(position, f"\u2022 {text}", "bullet")

    def insert_numbered(self, position, text):
        self.insert(position, f"{self.numbered_index}. {text}", "numbered")
        self.numbered_index += 1

    def insert_markdown(self, mkd_text):
        """A very basic markdown parser.

        Helpful to easily set formatted text in tk. If you want actual markdown
        support then use a real parser.
        """
        for line in mkd_text.split("\n"):
            if line == "":
                # Blank lines reset numbering
                self.numbered_index = 1
                self.insert("end", line)

            elif line.startswith("#"):
                tag = re.match(r"(#+) (.*)", line)
                line = tag.group(2)
                self.insert("end", line, tag.group(1))

            elif line.startswith("* "):
                line = line[2:]
                self.insert_bullet("end", line)

            elif line.startswith("1. "):
                line = line[2:]
                self.insert_numbered("end", line)

            elif not self.tag_char_re.search(line):
                self.insert("end", line)

            else:
                tag = None
                accumulated = []
                skip_next = False
                for i, c in enumerate(line):
                    if skip_next:
                        skip_next = False
                        continue
                    if c in self.tag_chars and (not tag or c == tag[0]):
                        if tag:
                            self.insert("end", "".join(accumulated), tag)
                            accumulated = []
                            tag = None
                        else:
                            self.insert("end", "".join(accumulated))
                            accumulated = []
                            tag = c
                            next_i = i + 1
                            if len(line) > next_i and line[next_i] == tag:
                                tag = line[i : next_i + 1]
                                skip_next = True

                    else:
                        accumulated.append(c)
                self.insert("end", "".join(accumulated), tag)

            self.insert("end", "\n")


class CustomTitleBar(Frame):
    def __init__(self, master, title="Custom Title Bar", close_callback=None):
        super().__init__(master, bg="#333333")
        self.master = master
        self.close_callback = close_callback

        self.resize_frame_top = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_v_double_arrow",
            height=2,
            fill=X,
            side=TOP,
        )
        self.title_label = Label(self, text=title, bg="#333333", fg="white", padx=10)
        self.title_label.pack(side=LEFT)

        self.close_button = Button(
            self, text="X", bg="#333333", fg="white", bd=0, command=self.close_window
        )
        self.close_button.pack(side=RIGHT)

        self.pack(fill=X)

        # 绑定鼠标事件
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<B1-Motion>", self.on_drag)

        self.resize_frame_bottom = ResizableFrame(
            self.master,
            bg="#A52A2A",
            cursor="sb_v_double_arrow",
            height=2,
            fill=X,
            side=BOTTOM,
        )
        self.resize_frame_left = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_h_double_arrow",
            width=2,
            fill=Y,
            side=LEFT,
        )
        self.resize_frame_right = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_h_double_arrow",
            width=2,
            fill=Y,
            side=RIGHT,
        )

    def close_window(self):
        if self.close_callback:
            self.close_callback()
        else:
            self.master.destroy()

    # 开始拖拽
    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    # 停止拖拽
    def stop_drag(self, event):
        self._drag_start_x = None
        self._drag_start_y = None

    # 拖拽中
    def on_drag(self, event):
        x = self.master.winfo_x() + event.x - self._drag_start_x
        y = self.master.winfo_y() + event.y - self._drag_start_y
        self.master.geometry(f"+{x}+{y}")


class CommonFrame(Frame):
    def __init__(
        self,
        master,
        bg,
        cursor,
        fill,
        side,
        width=None,
        height=None,
    ):
        super().__init__(master, bg=bg, cursor=cursor, width=width, height=height)
        self.fill = fill
        self.side = side
        self.pack(fill=fill, side=side)


class ResizableFrame(Frame):
    def __init__(
        self,
        master,
        bg,
        cursor,
        fill,
        side,
        width=None,
        height=None,
    ):
        super().__init__(master, bg=bg, cursor=cursor, width=width, height=height)
        self._resize_start_x = None
        self._resize_start_y = None
        self.bind("<B1-Motion>", self.resize)
        self.bind("<ButtonPress-1>", self.start_resize)
        self.bind("<ButtonRelease-1>", self.stop_resize)
        self.fill = fill
        self.side = side
        self.pack(fill=fill, side=side)

    def start_resize(self, event):
        if self.winfo_width() and self.winfo_height():
            self._resize_start_x = event.x_root
            self._resize_start_y = event.y_root

    def stop_resize(self, event):
        self._resize_start_x = None
        self._resize_start_y = None

    def resize(self, event):
        delta_x = 0
        delta_y = 0
        if self._resize_start_x is not None and self._resize_start_y is not None:
            if self.side in [LEFT, RIGHT]:
                delta_x = event.x_root - self._resize_start_x
            if self.side in [TOP, BOTTOM]:
                delta_y = event.y_root - self._resize_start_y

            if self.side == RIGHT:
                self.master.geometry(
                    f"{self.master.winfo_width()+ delta_x}x{self.master.winfo_height()+ delta_y}"
                )
            if self.side == LEFT:
                self.master.geometry(
                    f"{self.master.winfo_width()- delta_x}x{self.master.winfo_height()- delta_y}+{self.master.winfo_x() + delta_x}+{self.master.winfo_y() + delta_y}"
                )
            if self.side == TOP:
                self.master.geometry(
                    f"{self.master.winfo_width()- delta_x}x{self.master.winfo_height()- delta_y}+{self.master.winfo_x() + delta_x}+{self.master.winfo_y() + delta_y}"
                )
            if self.side == BOTTOM:
                self.master.geometry(
                    f"{self.master.winfo_width()+ delta_x}x{self.master.winfo_height()+ delta_y}"
                )

            self.start_resize(event)


class ActionSticky:
    """
    贴边隐藏功能
    """

    def __init__(self, master):
        self.master = master
        self.master.action_label.bind("<Enter>", self.show)
        self.master.action_label.bind("<Leave>", self.leave)

        # 窗口是否处于贴边隐藏状态
        self.is_sticky = False
        
        self.old_size = None

        self.direction = None
        # 贴边时，露出的大小
        self.sticky_length = 2

        self.min = 10

        # 鼠标是否在组件内
        self.mouse_is_in = False

        # 延时函数的id
        self.after_id = None


    def show(self, event):
        self.mouse_is_in = True
        # 取消最近的隐藏延迟
        if self.after_id:
            self.master.root.after_cancel(self.after_id)
            self.after_id = None

        if self.old_size and self.is_sticky:
            self.master.time_label.reset_default()
            self.master.time_label.update_time()

            self.master.action_label.reset_default()
            self.master.geometry(self.old_size[0], self.old_size[1])
            self.is_sticky = False

    def leave(self, event):
        self.mouse_is_in = False
        direction, x, y = self.is_sticky_to_right()
        # 检查窗口是否贴边
        if direction and not self.is_sticky:
            self.after_id = self.master.root.after(1000, self.hide)

    def hide(self):
        if self.mouse_is_in:
            return
        
        direction, x, y = self.is_sticky_to_right()

        if direction:
            self.animate_move(x, y)

            self.is_sticky = True

        if direction == "right":

            self.master.time_label.direction = 1  # 纵向
            self.master.time_label.place(x=13, y=0)
            # self.master.time_label.update_time()
        elif direction == "left":
            self.master.time_label.direction = 1  # 纵向
            self.master.time_label.place(
                x=self.master.action_label.winfo_x()
                + self.master.action_label.winfo_width(),
                y=0,
            )

        else:
            self.is_sticky = False

    def animate_move(self, x, y):
        current_x, current_y = (
            self.master.root.winfo_x(),
            self.master.root.winfo_y(),
        )
        steps = 20  # 增加步数
        dx = (x - current_x) / steps
        dy = (y - current_y) / steps
        self._move_step(0, steps, current_x, current_y, dx, dy, x, y)

    def _move_step(self, step, steps, current_x, current_y, dx, dy, target_x, target_y):
        if step < steps:
            new_x = int(current_x + dx * step)
            new_y = int(current_y + dy * step)
            self.master.geometry(new_x, new_y)
            # self.master.root.update_idletasks()  # 立即更新GUI
            self.master.root.after(
                10,
                self._move_step,
                step + 1,
                steps,
                current_x,
                current_y,
                dx,
                dy,
                target_x,
                target_y,
            )
        else:
            self.master.geometry(target_x, target_y)

    def is_sticky_to_right(self):
        # 屏幕宽度/高度
        screen_width = self.master.root.winfo_screenwidth()
        screen_height = self.master.root.winfo_screenheight()

        # 父宽度/高度
        father_width = self.master.root.winfo_width()
        father_height = self.master.root.winfo_height()

        # 宠物宽度/高度
        action_width = self.master.action_label.winfo_width()
        action_height = self.master.action_label.winfo_height()

        # 父位置
        father_x = self.master.root.winfo_x()
        father_y = self.master.root.winfo_y()

        # 宠物相对父位置
        action_x = self.master.action_label.winfo_x()
        action_y = self.master.action_label.winfo_y()

        # 宠物相对屏幕位置
        action_window_x = father_x + action_x
        action_window_y = father_y + action_y

        # 宠物最右侧相对屏幕位置
        action_right_x = action_window_x + action_width
        # 宠物最左侧相对屏幕位置
        action_left_x = action_window_x
        # 宠物最左侧相对屏幕位置
        action_top_y = action_window_y

        # 初始化坐标
        x, y = father_x, father_y
        self.direction = None

        # 计算宠物最右侧距离屏幕最右侧的距离
        distance_to_right = screen_width - action_right_x
        # 计算宠物最左侧距离屏幕最左侧的距离
        distance_to_left = action_left_x
        # 计算宠物最上侧距离屏幕最上侧的距离
        distance_to_top = action_top_y

        # 宠物最左侧贴边屏幕最右侧的位置
        edging_right = screen_width - action_x
        # 宠物最右侧贴边屏幕最左侧的位置
        edging_left = -action_x - action_width
        # 宠物最下侧贴边屏幕最上侧的位置
        # edging_top = -action_x - action_width

        # 判断距离是否小于5
        if distance_to_right < 5:
            self.direction = "right"
            # 屏幕宽度 - 宠物相对父位置（宠物左侧贴边）
            x = edging_right - self.sticky_length
            self.old_size = (
                screen_width - action_x - action_width + 10,
                y,
            )
        elif distance_to_left <5:
            self.direction = "left"
            x = edging_left + self.sticky_length +1
            self.old_size = (
                -action_x,
                y,
            )
        # elif distance_to_top<5 :
        #     self.direction = "top"

        else:
            self.old_size = None
        return self.direction, x, y

import re
import time
import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscroll
from log import setup_logger 


class SimpleMarkdownText(tkscroll.ScrolledText):
    """
    Really basic Markdown display. Thanks to Bryan Oakley's RichText:
    https://stackoverflow.com/a/63105641/79125
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkfont.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkfont.Font(**default_font.configure())
        italic_font = tkfont.Font(**default_font.configure())
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
            header_font = tkfont.Font(**default_font.configure())
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


class CustomTitleBar(tk.Frame):
    def __init__(self, master, title="Custom Title Bar", close_callback=None):
        super().__init__(master, bg="#333333")
        self.master = master
        self.close_callback = close_callback

        self.resize_frame_top = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_v_double_arrow",
            height=2,
            fill=tk.X,
            side=tk.TOP,
        )
        self.title_label = tk.Label(self, text=title, bg="#333333", fg="white", padx=10)
        self.title_label.pack(side=tk.LEFT)

        self.close_button = tk.Button(
            self, text="X", bg="#333333", fg="white", bd=0, command=self.close_window
        )
        self.close_button.pack(side=tk.RIGHT)

        self.pack(fill=tk.X)

        # 绑定鼠标事件
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<B1-Motion>", self.on_drag)

        self.resize_frame_bottom = ResizableFrame(
            self.master,
            bg="#A52A2A",
            cursor="sb_v_double_arrow",
            height=2,
            fill=tk.X,
            side=tk.BOTTOM,
        )
        self.resize_frame_left = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_h_double_arrow",
            width=2,
            fill=tk.Y,
            side=tk.LEFT,
        )
        self.resize_frame_right = ResizableFrame(
            self.master,
            bg="#333333",
            cursor="sb_h_double_arrow",
            width=2,
            fill=tk.Y,
            side=tk.RIGHT,
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


class ResizableFrame(tk.Frame):
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
            if self.side in [tk.LEFT, tk.RIGHT]:
                delta_x = event.x_root - self._resize_start_x
            if self.side in [tk.TOP, tk.BOTTOM]:
                delta_y = event.y_root - self._resize_start_y

            if self.side == tk.RIGHT:
                self.master.geometry(
                    f"{self.master.winfo_width()+ delta_x}x{self.master.winfo_height()+ delta_y}"
                )
            if self.side == tk.LEFT:
                self.master.geometry(
                    f"{self.master.winfo_width()- delta_x}x{self.master.winfo_height()- delta_y}+{self.master.winfo_x() + delta_x}+{self.master.winfo_y() + delta_y}"
                )
            if self.side == tk.TOP:
                self.master.geometry(
                    f"{self.master.winfo_width()- delta_x}x{self.master.winfo_height()- delta_y}+{self.master.winfo_x() + delta_x}+{self.master.winfo_y() + delta_y}"
                )
            if self.side == tk.BOTTOM:
                self.master.geometry(
                    f"{self.master.winfo_width()+ delta_x}x{self.master.winfo_height()+ delta_y}"
                )

            self.start_resize(event)


class StickyWindow:
    """
    贴边隐藏功能
    """
    def __init__(self, master):
        self.master = master
        self.master.attributes("-topmost", True)
        self.master.bind("<Enter>", self.show)
        self.master.bind("<Leave>", self.leave)
        # 窗口是否处于贴边隐藏状态
        self.is_sticky = False
        self.old_size = None

        self.show_nums = 0

        self.direction = None


    def show(self, event):
        self.show_nums += 1
        if self.show_nums == 1:
            if self.old_size and self.is_sticky:
                self.master.geometry(f"+{self.old_size[0]}+{self.old_size[1]}")
                self.is_sticky = False

    def leave(self, event):

        self.show_nums -= 1
        if self.show_nums == 0:
            # 检查窗口是否贴边
            if self.is_sticky_to_right() and not self.is_sticky:
                self.hide(event)

                
    def hide(self, event):
        direction = self.is_sticky_to_right()
        self.old_size = self.master.winfo_x(), self.master.winfo_y()
        if direction == "right":
            self.animate_move(self.master.winfo_screenwidth() - 2, self.master.winfo_y())
        if direction == "left":
            self.animate_move(2 - self.master.winfo_width(), self.master.winfo_y())
        if direction == "top":
            self.animate_move(self.master.winfo_x(), 2 - self.master.winfo_height())
        self.is_sticky = True
        self.show_nums = 0
    def animate_move(self, x, y):
        current_x, current_y = self.master.winfo_x(), self.master.winfo_y()
        steps = 10  # 增加步数
        dx = (x - current_x) / steps
        dy = (y - current_y) / steps
        for i in range(steps):
            self.master.geometry(f"+{int(current_x + dx * i)}+{int(current_y + dy * i)}")
            self.master.update_idletasks()
            self.master.after(10)  # 设置每步之间的时间间隔，单位为毫秒
        self.master.geometry(f"+{x}+{y}")

    def is_sticky_to_right(self):

        screen_width = self.master.winfo_screenwidth()
        window_width = self.master.winfo_width()
        window_x = self.master.winfo_x()
        window_y = self.master.winfo_y()
        self.direction = None
        if window_x + window_width >= screen_width - 5:
            self.direction = "right"
        if window_x <= 5:
            self.direction = "left"
        if window_y <= 5:
            self.direction = "top"
        return self.direction

class WebviewStickyWindow(StickyWindow):
    """
    在有webview时的贴边隐藏功能w
    """
    def __init__(self, master):
        super().__init__(master)

        self.show_check_funcs = []
        self.level_check_funcs = []


        # self.check_level()

        self.after_id = None

        self.before_flag = None

        self.show_nums = 0
        self.master.after(5000,self.init_show_num)

        self.events = []
        self._time = time.time()

        self.reversal_time = time.time()

    def init_show_num(self):
        self.show_nums = 0

    def show(self, event):
        self._time = time.time()
        self.show_nums += 1
        if self.show_nums == 1:
            if self.old_size and self.is_sticky:
                self.master.geometry(f"+{self.old_size[0]}+{self.old_size[1]}")
                self.is_sticky = False

    def leave(self, event):
        self._time = time.time()

        if self.show_nums:
            self.show_nums -= 1

    def check_master_mouse_in(self,event):
        for i in self.level_check_funcs:
            flag = i(event)
            if not flag:
                return True
        return False

    def _level(self,event):
        if self.check_master_mouse_in(event):
            return
        if time.time() - self._time <1:
            return

        if self.show_nums == 0:
            # 检查窗口是否贴边
            if self.is_sticky_to_right() and not self.is_sticky:
                self.hide(event)


    def hide(self, event):
        if self.check_master_mouse_in(event):
            return
        if time.time() - self._time <1:
            return

        return super().hide(event)
    
    def _hide(self):
        return super().hide(None)

    def reversal(self):
        try:
            if self.is_sticky:
                self.show_nums = 0
                self.show(None)
            else:
                super().hide(None)
        except Exception as e:
            WebLogger.info("reversal error:{}".format(e))
            
    def check_level(self):
        try:
            self._level(None)
        except:
            pass
        self.after_id = self.master.after(1000,self.check_level)
class WebLogger:
    logger = None

    @classmethod
    def info(cls, msg, *args, **kwargs):
        if not cls.logger:
            cls.logger = setup_logger()
        cls.logger.info(msg, *args, **kwargs)


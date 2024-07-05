from tkinter import Toplevel, WORD, BOTH
from .common import CustomTitleBar, SimpleMarkdownText


class TextPopup(Toplevel):
    """
    一个置顶的小文本提示框弹窗
    """

    def __init__(self, master, destroy_time=3000, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.window_width = 200
        self.window_height = 100
        self.overrideredirect(True)
        self.title("")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.8)  # 设置透明度为0.5，取值范围为0.0到1.0
        self.attributes("-toolwindow", True)
        self.title_bar = CustomTitleBar(self, title="消息提示")
        self.text = SimpleMarkdownText(self, wrap=WORD)
        self.text.hide_vertical_scrollbar()
        self.text.pack(expand=True, fill=BOTH)

        self.set_size()

        self.after(destroy_time, self.destroy)

    def add_text(self, text):
        self.text.insert_markdown(text)

    def set_size(self):
        """
        初始化大小/位置
        """
        # 获取屏幕尺寸
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 计算初始位置
        init_x = self.master.winfo_x()
        init_y = self.master.winfo_y() - 100

        # 窗口宽度和高度
        window_width = self.window_width
        window_height = self.window_height

        # 确保窗口在屏幕范围内
        if init_x < 0:
            init_x = 0
        elif init_x + window_width > screen_width:
            init_x = screen_width - window_width

        if init_y < 0:
            init_y = 0
        elif init_y + window_height > screen_height:
            init_y = screen_height - window_height

        self.geometry(f"{window_width}x{window_height}+{init_x}+{init_y}")
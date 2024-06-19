import tkinter
from .common import  CustomTitleBar, SimpleMarkdownText




class TextPopup(tkinter.Toplevel):
    """
    一个置顶的文本提示框弹窗
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
        self.text = SimpleMarkdownText(self, wrap=tkinter.WORD)
        self.text.hide_vertical_scrollbar()
        self.text.pack(expand=True, fill=tkinter.BOTH)
        self.geometry(
            "%dx%d+%d+%d"
            % (
                self.window_width,
                self.window_height,
                self.master.winfo_x(),
                self.master.winfo_y() - 100,
            )
        )
        self.after(destroy_time, self.destroy)

    def add_text(self, text):
        self.text.insert_markdown(text)

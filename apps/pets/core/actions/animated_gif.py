import tkinter


class AnimatedGIF(tkinter.Label):
    def __init__(self, canvas, frames, delay=0, *args, **kwargs) -> None:
        super().__init__(master=canvas, bd=0, bg="black", *args, **kwargs)
        self.bg = "black"
        self.canvas = canvas
        self.delay = delay
        self.frames = frames
        self.frame_num = 0
        self.is_start = False
        self.after_id = None
        self.animate()

    def update_frames(self, frames):
        # 取消先前的动画定时器
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.frames = frames
        self.frame_num = 0
        self.animate()

    def animate(self):
        try:
            if not self.frames:
                self.frame_num = 0
                return self.master.after(100, self.animate)

            if self.frame_num + 1 < len(self.frames):
                self.frame_num += 1
                self.is_start = True
                image = self.frames[self.frame_num][0]
                self.config(image=image)
                delay = self.frames[self.frame_num][1]
                self.after_id = self.master.after(
                    self.frames[self.frame_num][1] if delay != 0 else 100, self.animate
                )
            else:
                self.is_start = False

        except Exception as e:
            print(e)


class RotateImage(tkinter.Label):
    def __init__(self, canvas, image, delay=0, *args, **kwargs) -> None:
        super().__init__(master=canvas, bd=0, bg="black", *args, **kwargs)
        self.bg = "black"
        self.canvas = canvas
        self.delay = delay
        self.image
        self.frame_num = 0
        self.is_start = False
        self.after_id = None
        self.animate()

    def animate(self):
        try:
            if not self.frames:
                self.frame_num = 0
                return self.master.after(100, self.animate)

            if self.frame_num + 1 < len(self.frames):
                self.frame_num += 1
                self.is_start = True
                image = self.frames[self.frame_num][0]
                self.config(image=image)
                delay = self.frames[self.frame_num][1]
                self.after_id = self.master.after(
                    self.frames[self.frame_num][1] if delay != 0 else 100, self.animate
                )
            else:
                self.is_start = False

        except Exception as e:
            print(e)

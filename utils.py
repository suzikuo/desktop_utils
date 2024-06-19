from kernel.settings import IMG_DIR


def get_image(filename):
    return IMG_DIR + "/" + filename


def set_default_size(*args):
    from kivy.core.window import Window

    Window.left = Window.width
    Window.top = 50
    Window.size = (400, 700)

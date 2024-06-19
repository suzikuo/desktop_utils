from log import MyLogger


def show_message(message, title="提示"):
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, title, 0)
    except Exception as e:
        MyLogger.error(f"[Show Message] {e}")
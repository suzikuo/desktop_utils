import os
import sys
from kernel.message import show_message

from log import MyLogger

# 定义进程锁文件路径
LOCK_FILE = "./app.lock"


def run():
    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except FileExistsError:
        show_message("程序正在运行")
        MyLogger.info("[os.open] app正在运行...")
        sys.exit(0)

    from kernel.app import MyApp
    app = MyApp()
    try:
        app.run()
    except ValueError as v:
        show_message(str(v))
    except Exception as e:
        MyLogger.error("[app.run] error:{}".format(e))
        show_message("启动失败")
        app.stop()

    try:
        os.close(lock_fd)
    except Exception as e:
        MyLogger.error("[os.close] error:{}".format(e))
    os.remove(LOCK_FILE)
    # 强制关闭
    # os._exit(0)

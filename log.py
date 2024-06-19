import logging


def setup_logger() -> logging.Logger:
    # 1、设置全局的日志格式和级别
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    # 2、获取logger （给日志器起个名字 "__name__"）
    MyLogger = logging.getLogger(
        __name__
    )  # __name__内置变量模块名称，轻松地识别出哪个模块产生了哪些日志消息（主程序模块）
    # 3、创建文件处理器，指定日志文件和日志级别（局部）---文件输出FileHandle（输出到指定文件）
    file_handler = logging.FileHandler(
        "application.log"
    )  # 指定日志文件名application.log，默认在当前目录下创建
    file_handler.setLevel(logging.INFO)  # 设置日志级别(只输出对应级别INFO的日志信息)
    # 设置日志格式
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%m/%d/%Y %H:%M:%S"
        )
    )

    error_handler = logging.FileHandler(
        "error.log"
    )  # 指定日志文件名error.log，默认在当前目录下创建
    error_handler.setLevel(logging.ERROR)  # 设置日志级别(只输出对应级别INFO的日志信息)
    # 设置日志格式
    error_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%m/%d/%Y %H:%M:%S"
        )
    )

    # 4、添加文件处理器到logger
    MyLogger.addHandler(file_handler)
    MyLogger.addHandler(error_handler)

    return MyLogger


MyLogger = setup_logger()

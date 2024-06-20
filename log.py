import logging

from logging.handlers import RotatingFileHandler


def setup_logger() -> logging.Logger:
    # 设置全局的日志格式和级别
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    # 获取logger
    MyLogger = logging.getLogger(__name__)

    # 创建文件处理器，指定日志文件和日志级别（局部）---文件输出FileHandle（输出到指定文件）
    file_handler = RotatingFileHandler(
        "application.log",
        maxBytes=1 * 1024 * 1024,  # 设置最大文件大小为1MB
        backupCount=0,  # 不保留备份文件，覆盖写
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%m/%d/%Y %H:%M:%S"
        )
    )

    error_handler = RotatingFileHandler(
        "error.log",
        maxBytes=1 * 1024 * 1024,  # 设置最大文件大小为1MB
        backupCount=0,  # 不保留备份文件，覆盖写
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%m/%d/%Y %H:%M:%S"
        )
    )

    # 添加文件处理器到logger
    MyLogger.addHandler(file_handler)
    MyLogger.addHandler(error_handler)

    return MyLogger


MyLogger = setup_logger()

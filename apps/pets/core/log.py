from log import setup_logger


class PetLogger:
    logger = None

    @classmethod
    def info(cls, msg, *args, **kwargs):
        if not cls.logger:
            cls.logger = setup_logger()
        cls.logger.info(msg, *args, **kwargs)
    @classmethod
    def error(cls, msg, *args, **kwargs):
        if not cls.logger:
            cls.logger = setup_logger()
        cls.logger.error(msg, *args, **kwargs)


def init_pet_logger():
    PetLogger.logger = setup_logger()

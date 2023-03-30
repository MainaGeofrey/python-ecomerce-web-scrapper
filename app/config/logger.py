import logging.config


class LevelOnlyFilter:
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {  # root logger
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stream_handler", "file_handler"],
        },
        "custom_logger": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stream_handler"],
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
            "filters": ["only_warning"],
            "formatter": "default_formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "../logs/scrap.log",
            "mode": "a",
            "level": "DEBUG",
            "formatter": "default_formatter",
        },
    },
    "filters": {
        "only_warning": {
            "()": LevelOnlyFilter,
            "level": logging.WARN,
        },
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s",
        },
    },
}

"""logging.debug()
logging.info()
logging.warning()
logging.error()
logging.critical()"""
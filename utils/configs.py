
class Variables:
    url: str = "https://www.chess.com/home"
    
    logger_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s(%(name)s): %(message)s",
                "datefmt": "%d/%m/%Y %H:%M:%S",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": "execution.log",
                "mode": "a",
                "encoding": "utf-8",
                "formatter": "default",
            }
        },
        "loggers": {
            "": {
                "level": "DEBUG",
                "handlers": ["file"],
            }
        },
    }

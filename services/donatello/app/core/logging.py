import logging
import logging.config


def configure_logging():
    logging_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s [%(levelname)s] [%(name)s:%(lineno)s] %(funcName)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "propagate": True,
            },
            "uvicorn": {
                "propagate": True,
            }
        },
    }

    logging.config.dictConfig(logging_dict)
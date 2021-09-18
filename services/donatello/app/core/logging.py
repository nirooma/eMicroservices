import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # "format": "[%(asctime)s: %(levelname)s] [%(pathname)s:%(lineno)d] %(message)s",
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
        "root": {
            "handlers": ["console"],
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn": {
            "propagate": True,
        },
    },
})



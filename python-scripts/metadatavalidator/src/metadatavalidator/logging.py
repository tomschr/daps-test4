import logging

#: The logger name; can also set to "__name__"
LOGGERNAME = "metadata"


#: The dictionary, passed to :class:`logging.config.dictConfig`,
#: is used to setup your logging formatters, handlers, and loggers
#: For details, see https://docs.python.org/3.4/library/logging.config.html#configuration-dictionary-schema
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {'format': '[%(levelname)s] %(funcName)s: %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', # will be set later
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        LOGGERNAME: {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Set the root logger's log level:
        'root': {
            'level': 'WARNING',
            'handlers': ["console"],
        }
    }
}


#: Map verbosity level (int) to log level
LOGLEVELS = {None: logging.WARNING,  # 0
             0: logging.WARNING,
             1: logging.INFO,
             2: logging.DEBUG,
             }


#: Instantiate our logger
log = logging.getLogger(LOGGERNAME)
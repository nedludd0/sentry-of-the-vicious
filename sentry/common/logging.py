"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
import logging
import logging.config

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
from sentry.config import LOG_PATH_MAIN

# CONFIG
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {  # root logger
            'handlers': ['console_handler'],
        },
        'myLogFileMain': {  # application logger main on file
            'propagate': True,
            'handlers': ['file_handler_main'],
            'qualname': 'myLogFileMain',
        },     
        'myLogConsole': {  # application logger on console
            'handlers': ['console_handler'],
            'qualname': 'myLogConsole',
        }  
    },
    'handlers': {
        'console_handler': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file_handler_main': {
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH_MAIN,
            'maxBytes': 1048576, # 1MB
            'backupCount': 7,
            'mode': 'a',
        }  
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] - [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

# LOGGER main
my_logger_main = logging.getLogger('myLogFileMain')

"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
from os import environ

#################### COMMON ####################

### GENERAL
FOLLOWSTRATEGY_ENV = environ.get('FOLLOWSTRATEGY_ENV')

### DATABASE
DB_TYPE = environ.get('DB_TYPE')

### TIMEZONE
TIMEZONE = 'Europe/Rome'

### TG BOT
# https://core.telegram.org/bots/api#markdownv2-style
# https://core.telegram.org/bots/api#html-style
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.parsemode.html
TG_BOT_PARSE_MODE = ParseMode.HTML # MARKDOWN (Markdown) or MARKDOWN_V2 (MarkdownV2) or HTML (HTML)

#################### SPECIFIC ####################

if FOLLOWSTRATEGY_ENV == 'development':

    ### DATABASE
    DB_SCHEMA = environ.get('DB_SCHEMA_DEV')
    DB_SCHEMA_PATH = environ.get('DB_SCHEMA_PATH_DEV')

    ### LOGGING
    LOG_PATH_MAIN=environ.get('LOG_PATH_MAIN_DEV')
    LOG_LEVEL_MAIN='DEBUG' # DEBUG, INFO, WARNING, ERROR or CRITICAL

    ##### PTB
    TG_BOT_NAME= environ.get('TG_BOT_NAME_DEV')
    TG_BOT_TOKEN = environ.get('TG_BOT_TOKEN_DEV')

elif FOLLOWSTRATEGY_ENV == 'production':
    
    ### DATABASE
    DB_SCHEMA = environ.get('DB_SCHEMA_PROD')
    DB_SCHEMA_PATH = environ.get('DB_SCHEMA_PATH_PROD')

    ### LOGGING
    LOG_PATH_MAIN=environ.get('LOG_PATH_MAIN_PROD')
    LOG_LEVEL_MAIN='INFO' # DEBUG, INFO, WARNING, ERROR or CRITICAL

    ##### PTB
    TG_BOT_NAME= environ.get('TG_BOT_NAME_PROD')
    TG_BOT_TOKEN = environ.get('TG_BOT_TOKEN_PROD')


#################### BUILD DB URLS ####################

SQLALCHEMY_URL = f"{DB_TYPE}:////{DB_SCHEMA_PATH_DEV}/{DB_SCHEMA}.db"


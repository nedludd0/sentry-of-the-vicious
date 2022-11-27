"""""""""""""""""""""""""""
IMPORT from VENV
"""""""""""""""""""""""""""
## Log
import logging

"""""""""""""""""""""""""""
IMPORT from My Project
"""""""""""""""""""""""""""
## Common
from followstrategy import config
## My Logger
from followstrategy.common.logging import my_logger_main
## FLASK APP (web app)
from followstrategy.web_console import create_app_4flask


"""""""""""""""
CONF LOGGING
"""""""""""""""

## IMPORTANTE: questo è solo per my_logger_main che vive dentro il processo principale (proj)
## se vuoi usare l'altro logger my_logger_celery_worker (cioè quello che vive dentro il processo dei worker celery)
## devi configurare in followstrategy/common/celery/start_celery_workers.py

# Set Log Level
my_logger_main.setLevel(config.LOG_LEVEL_MAIN)
# Varius Logger
for logger in ( logging.getLogger('werkzeug'), #logging.getLogger('pyrogram'), logging.getLogger('sqlalchemy')
                logging.getLogger('telegram.bot'),
                logging.getLogger('telegram.ext'),
                logging.getLogger('telegram.ext.updater'),
                logging.getLogger('telegram.ext.dispatcher')    ):
    logger.handlers = my_logger_main.handlers
    logger.setLevel(my_logger_main.level)  

"""""""""""""""
EXECUTE PROJECT
"""""""""""""""

# IF EXECUTE PYTHON -M FOLLOWSTRATEGY
if __name__ == '__main__':

    """ START FLASK_APP """
    flask_app = create_app_4flask( logger_overwrite = my_logger_main )
    
    """START BJOERN (wsgi server) """
    import bjoern
    # Get Values
    host = config.BJOERN_HOST
    port = config.BJOERN_PORT
    socket = config.BJOERN_SOCKET
    # Run Bjoern
    if host is not None and port is not None:
        # Bind to Ip/Port
        bjoern.run(flask_app, host, int(port))
    elif socket is not None:
        # Bind to Unix socket
        bjoern.run(flask_app, f"unix:{socket}")

# IF EXECUTE WITH FLASK RUN
else:
    
    """ START FLASK_APP """
    flask_app = create_app_4flask( logger_overwrite = my_logger_main )
    

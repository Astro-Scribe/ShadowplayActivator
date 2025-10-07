from loguru import logger
import os
import sys

log_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'ShadowPlayActivator') # like this: C:\users\username\appdata\local\temp\shadowplayactivator
os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, f'shadowplay_activator.log')
with open(LOG_FILE_PATH, 'w'):
    pass

_is_configured = False

def configure_logger():
    """
    Configure the logger just once
    """
    global _is_configured

    if _is_configured:
        return

    log_level = "DEBUG" if len(sys.argv) > 1 and sys.argv[1] == 'd' else "INFO"
    rotation = "5 MB"
    retention = 1

    logger.remove()

    logger.add(
        LOG_FILE_PATH, 
        format="{time:YYYY-MM-DDTHH:mm:ss.SSS}-{level}-{name}: {message}", 
        level=log_level, 
        rotation=rotation, 
        retention=retention
    )
    _is_configured = True
    print(f"Log file: {LOG_FILE_PATH}")

def get_logger(name):
    """
    Returns a logger with the specified name.\n
    Automatically configures logger if not already configured.\n
    
    Usage:
    - logger = get_logger("MyScriptName")
    """
    if not _is_configured:
        configure_logger()
    
    return logger.patch(lambda record: record.update(name=name))



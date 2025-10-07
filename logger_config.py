from loguru import logger
import os

log_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'ShadowPlayActivator') # like this: users\username\appdata\local\temp\shadowplayactivator
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f'shadowplay_activator.log')
with open(log_path, 'w'):
    pass

logger.remove()
logger.add(sink=log_path)

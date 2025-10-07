"""A very patient and simple script that mimics the hotkey press 'Alt+Shift+F10' to turn on your Shadowplay, unless it is already active!
(MAKE SURE YOUR HOTKEY FOR ACTIVATION IS ALT+SHIFT+F10!)
"""

import time
import sys
import os

from spa.utils.monitor import shadowplay_is_running
from spa.utils.utility import add_to_startup_programs, is_session_active, wait_for_desktop_ready
from spa.utils.logger_config import get_logger
from spa.utils.key_inputs import press_key_combination

logger = get_logger('Shadowplay Activator')

def activate_shadowplay():
    """Activate NVIDIA ShadowPlay by pressing Alt+Shift+F10"""
    logger.info("Activating NVIDIA ShadowPlay with Alt+Shift+F10...")
    # Press Alt+Shift+F10
    press_key_combination()
    logger.info("Key combination sent!")

def main():
    wait_for_desktop_ready()
    start = time.time()
    i = 0
    while not is_session_active() and time.time() - start < 3600: # 1 hr (length of time the program waits before you have logged in as hotkey may not be registered if entered when not logged in)
        if i < 10:
            logger.debug("Session is not active. Waiting for active session...")
            i += 1
        elif i == 10:
            logger.debug("Session has been inactive for a while so will no longer be reporting as such.")
        time.sleep(5)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'd':
        logger.debug("Running in debug mode; skipping usual 30s wait.")
        time.sleep(0.1)
    else:
        time.sleep(30)
    #NOTE shadowplay appears to be (sometimes..) turning itself OFF automatically if it starts as on??
    # so, we wait until well after that check has occured. 30 seconds has been sufficient in my (limited) testing

    if shadowplay_is_running():
       logger.info("Shadowplay is already on!")
    else:
        activate_shadowplay()

if __name__ == "__main__":
    try:
        if getattr(sys, 'frozen', False):
            add_to_startup_programs(path=os.path.abspath(sys.executable))
        else:
            logger.debug("Running as python script, so not adding to startup programs.")
        
        main()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


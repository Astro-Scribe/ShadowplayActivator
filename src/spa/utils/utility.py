import winreg
from win32 import win32ts
import time
import psutil

from spa.utils.logger_config import get_logger

logger = get_logger("Utility")

def add_to_startup_programs(path):
    try:
        logger.debug(f"Path to exe being added to startup programs: {path}")
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "shadowplay_activator", 0, winreg.REG_SZ, f'"{path}"')
    except Exception as e:
        logger.error(f"Error while adding to startup: {e}")

def is_session_active():
    """
    Check if the current session is active (not locked or disconnected)
    """
    try:
        session_id = win32ts.WTSGetActiveConsoleSessionId()
        return session_id != 0xFFFFFFFF
    except Exception as e:
        logger.info(f"Error while checking if session is active: {str(e)}")
        return True

def wait_for_desktop_ready():
    """Wait until the Windows desktop is fully loaded and ready for input"""
    timeout = 180  # seconds
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if any("explorer.exe" in p.name().lower() for p in psutil.process_iter(['name'])):
            # Explorer is running, give it a bit more time to fully initialize
            time.sleep(0.5)
            return True
        time.sleep(1)
    
    return False


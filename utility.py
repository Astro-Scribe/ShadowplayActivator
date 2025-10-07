import winreg
from logger_config import logger

def add_to_startup_programs(path):
    try:
        print(f"Path to exe being added to startup programs: {path}")
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "shadowplay_activator", 0, winreg.REG_SZ, f'"{path}"')
    except Exception as e:
        logger.error(f"Error while adding to startup: {e}")


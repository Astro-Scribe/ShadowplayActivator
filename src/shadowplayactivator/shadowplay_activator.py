"""A very patient and simple program that mimics the hotkey press 'Alt+Shift+F10' to turn on your Shadowplay, unless it is already active!
(i.e. MAKE SURE YOUR HOTKEY FOR ACTIVATION IS ALT+SHIFT+F10!)
"""

import time
import ctypes
import sys
import os
import psutil
from win32 import win32ts

from shadowplayactivator.monitor import shadowplay_is_running
from shadowplayactivator.utils.utility import add_to_startup_programs
from shadowplayactivator.utils.logger_config import logger, log_path

# Define constants for key codes
ALT = 0x12
SHIFT = 0x10
F10 = 0x79

# Define SendInput structure and functions from user32.dll
PUL = ctypes.POINTER(ctypes.c_ulong)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("union", INPUT_UNION)
    ]

# Constants for SendInput
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

# Load user32.dll
user32 = ctypes.WinDLL('user32')
user32.SendInput.argtypes = (ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int)
user32.SendInput.restype = ctypes.c_uint

def send_key_event(key_code, key_up=False):
    """Send a key event (press or release)"""
    extra = ctypes.c_ulong(0)
    flags = KEYEVENTF_KEYUP if key_up else 0
    
    input_struct = INPUT(
        type=INPUT_KEYBOARD,
        union=INPUT_UNION(
            ki=KEYBDINPUT(
                wVk=key_code,
                wScan=0,
                dwFlags=flags,
                time=0,
                dwExtraInfo=ctypes.pointer(extra)
            )
        )
    )
    
    user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))

def press_key_combination(keys):
    """Press and release a combination of keys"""
    # Press all keys in the combination
    for key in keys:
        send_key_event(key)
    
    # Small delay to ensure the combination is registered
    time.sleep(0.1)
    
    # Release all keys in reverse order
    for key in reversed(keys):
        send_key_event(key, key_up=True)

def activate_shadowplay():
    """Activate NVIDIA ShadowPlay by pressing Alt+Shift+F10"""
    logger.info("Activating NVIDIA ShadowPlay with Alt+Shift+F10...")
    # Press Alt+Shift+F10
    press_key_combination([ALT, SHIFT, F10])
    logger.info("Key combination sent!")

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
    # Wait for explorer.exe to be running
    timeout = 180  # seconds
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if any("explorer.exe" in p.name().lower() for p in psutil.process_iter(['name'])):
            # Explorer is running, give it a bit more time to fully initialize
            time.sleep(5)
            return True
        time.sleep(1)
    
    return False

def main():
    # Wait for desktop to be fully loaded
    wait_for_desktop_ready()
      
    # Check if session is active
    start = time.time()
    i = 0
    while not is_session_active() and time.time() - start < 3600: # 1 hr (length of time the program waits before you have logged in as hotkey may not be registered if entered when not logged in)
        if i < 10:
            logger.info("Session is not active. Waiting for active session...")
            i += 1
        elif i == 10:
            logger.info("Session has been inactive for a while so will no longer be reporting as such.")
        time.sleep(5)  # Wait and check again
    
    time.sleep(30)  # shadowplay appears to be (sometimes..) turning itself OFF automatically if it starts as on??
    # so, we wait until well after that check has occured. 30 seconds has been sufficient in my (limited) testing
    if shadowplay_is_running():
       logger.info("Shadowplay is already on!")
    else:
        activate_shadowplay()

if __name__ == "__main__":
    try:
        print(f"Log file: {log_path}")

        if getattr(sys, 'frozen', False):
            add_to_startup_programs(path=os.path.abspath(sys.executable))
        else:
            logger.info("Running as python script, so not adding to startup programs.")
        
        main()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
  
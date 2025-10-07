import ctypes
import time


ALT = 0x12
SHIFT = 0x10
F10 = 0x79

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

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

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

def press_key_combination(keys=[ALT, SHIFT, F10]):
    """Press and release a combination of keys

    Args:
        keys (list, optional): The keys to press and release. Defaults to [ALT, SHIFT, F10].
    """
    for key in keys:
        send_key_event(key)
    
    time.sleep(0.1)
    
    for key in reversed(keys):
        send_key_event(key, key_up=True)

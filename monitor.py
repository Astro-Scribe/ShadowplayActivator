import os
from pathlib import Path
import time

def check_temp_recording_files():
    """Check if any temporary recording file(s) are being actively written"""
    temp_paths = [
        Path(os.environ.get('LOCALAPPDATA', '')) / "Temp", #NOTE: this is the default for the new app. Unfortunate that it's not nvidia specific.. but whatever ig
    ]
    # example file: AppData\Local\Temp\9343b833-e7af-42ea-8a61-31bc41eefe2b\ShaE692.tmp
    for temp_path in temp_paths:
        if temp_path.exists():
            for file in temp_path.rglob('*'):
                if file.is_file() and file.suffix in ['.tmp', '.mp4']:
                    if time.time() - file.stat().st_mtime < 10:
                        print(f" Found active recording file: {file}")
                        return True
    
    return False

def shadowplay_is_running() -> bool:
    """Returns True if shadowplay is already running, False if not."""
    results = {}
    
    results['temp_recording_file'] = check_temp_recording_files()
    
    for method, result in results.items():
        print(f"{method}: {result}")
    
    overall = any(results.values())
    
    return overall

if __name__ == "__main__":
    print(f"\nOverall result:\n    Shadowplay is running: {shadowplay_is_running()}")


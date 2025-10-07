import os
from pathlib import Path
import time
import re

from spa.utils.logger_config import get_logger

logger = get_logger("Monitor")

def check_temp_recording_files():
    """Check if any temporary recording file(s) are being actively written\n
    Assumes the temp file is within a uuid-named subdir in the temp dir."""
    # UUID/GUID pattern: 8-4-4-4-12 hexadecimal format
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    # seems to be this file pattern (e.g., "ShaE692.tmp")
    shadowplay_file_pattern = re.compile(r'^Sha[0-9A-F]{4}\.tmp$', re.IGNORECASE)
    
    temp_path = Path(os.environ.get('LOCALAPPDATA', '')) / "Temp"
    logger.debug(f"Temp path is: {temp_path}")
    
    if not temp_path.exists():
        logger.info(f"Temp path not found, hence must not be currently recording")
        return False
    
    for subdir in temp_path.iterdir():
        if subdir.is_dir() and uuid_pattern.match(subdir.name):
            for file in subdir.iterdir():
                if file.is_file():
                    if shadowplay_file_pattern.match(file.name):
                        logger.debug(f"Found file matching shadowplay file pattern: {file.name} ({file})")
                        if time.time() - file.stat().st_mtime < 10:
                            logger.info(f"check_temp_recording_files:    Found active recording file: {file}")
                            return True
                    elif file.suffix in ['.tmp', '.mp4']:
                        if time.time() - file.stat().st_mtime < 10:
                            logger.info(f"check_temp_recording_files:    Found active recording file: {file}")
                            return True
    
    return False

def shadowplay_is_running() -> bool:
    """Returns True if shadowplay is already running, False if not."""
    results = {}
    
    results['temp_recording_file'] = check_temp_recording_files()
    
    overall = any(results.values())
    
    return overall

if __name__ == "__main__":
    logger.info(f"Shadowplay is running: {shadowplay_is_running()}")


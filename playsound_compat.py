import playsound as _playsound
from pathlib import Path

# Workaround for the issue that playsound 1.3.0 does not handle relative paths on Windows
def playsound(file_path, block=True):
    # Convert to absolute path if it's a relative path
    abs_path = str(Path(file_path).resolve())
    try:
        _playsound.playsound(abs_path, block=block)
    except Exception as e:
        print(f"Error playing sound: {e}")
import playsound as _playsound
from pathlib import Path

def playsound(file_path, block=True):
    # Convert to absolute path if it's a relative path
    abs_path = str(Path(file_path).resolve())
    try:
        _playsound.playsound(abs_path, block=block)
    except Exception as e:
        print(f"Error playing sound: {e}")
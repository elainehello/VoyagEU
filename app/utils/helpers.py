import os
import json
from config.settings import DATA_PATH

def load_mock(filename: str):
    """
    Safely load mock data from a JSON file in the DATA_PATH directory.
    Prevents path traversal attacks by rejecting filenames with path separators.
    """
    # Only allow filenames without path separators
    if os.path.sep in filename or os.path.altsep and os.path.altsep in filename:
        raise ValueError("Invalid filename: path separators are not allowed.")
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
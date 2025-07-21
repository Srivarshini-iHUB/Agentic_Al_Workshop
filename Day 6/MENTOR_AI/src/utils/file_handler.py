import json
import os
from ..config.settings import TASKS_FILE

def save_result(result, filename=TASKS_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(result)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2) 
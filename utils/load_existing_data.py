import os
import json

def load_existing_data(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Папка utils
    src_dir = os.path.join(base_dir, "..", "src")
    full_path = os.path.join(src_dir, filename)

    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

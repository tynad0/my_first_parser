import json
import os
from pathlib import Path

def save_to_json(filename, data):
   
    src_dir = Path(__file__).parent.parent / "src"
    
    src_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = src_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Данные успешно сохранены в {file_path}")
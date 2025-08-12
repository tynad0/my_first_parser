from pathlib import Path
import pandas as pd
import os

def save_to_excel(filename, news_data):

    src_dir = Path(__file__).parent.parent / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    file_path = src_dir / filename


    if not isinstance(news_data, list):
        news_data = [news_data] 
    
    rows = []
    for item in news_data:
        if isinstance(item, str):
            rows.append({
                'Title': item,
                'Date': '',
                'News Link': '',
                'Author': '',
                'Author Link': ''
            })
        elif isinstance(item, dict):
            rows.append({
                'Date': item.get('date', ''),
                'Title': item.get('title', ''),
                'News Link': item.get('news_link', ''),
                'Author': item.get('author', ''),
                'Author Link': item.get('author_link', '')
            })
    
    df = pd.DataFrame(rows)
    
    try:
        existing_df = pd.read_excel(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(filename, index=False)
        print(f"Данные добавлены в {filename}")
    except FileNotFoundError:
        df.to_excel(file_path, index=False)
        print(f"Создан новый файл {file_path}")
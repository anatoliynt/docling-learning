"""
Проверка наличия таблиц в JSON файлах
"""

import json
from pathlib import Path


OUTPUT_DIR = Path("output")


def check_json_for_tables(json_file):
    """Проверяет JSON файл на наличие таблиц"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ищем таблицы в main_text
    tables = []
    for item in data.get('main_text', []):
        if item.get('type') == 'table':
            tables.append(item)
    
    # Также проверяем tables (если есть отдельная секция)
    if 'tables' in data:
        tables.extend(data['tables'])
    
    return tables


def main():
    print()
    print("=" * 70)
    print("🔍 ПРОВЕРКА ТАБЛИЦ В JSON")
    print("=" * 70)
    print()
    
    json_files = list(OUTPUT_DIR.glob("*.json"))
    json_files = [f for f in json_files if not f.name.endswith('_tables.json')]
    
    if not json_files:
        print("❌ JSON файлы не найдены в output/")
        return
    
    total_tables = 0
    
    for json_file in json_files:
        tables = check_json_for_tables(json_file)
        total_tables += len(tables)
        
        if tables:
            print(f"📄 {json_file.name}")
            print(f"   ✅ Найдено таблиц: {len(tables)}")
            for i, table in enumerate(tables, 1):
                num_rows = len(table.get('data', {}).get('table_cells', []))
                print(f"      Таблица {i}: {num_rows} ячеек")
        else:
            print(f"📄 {json_file.name}")
            print(f"   ⚠️  Таблиц не найдено")
        print()
    
    print("=" * 70)
    print(f"📊 ИТОГО: {total_tables} таблиц в {len(json_files)} файлах")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

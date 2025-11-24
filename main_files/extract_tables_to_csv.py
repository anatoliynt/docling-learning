"""
Извлечение таблиц из JSON в CSV (на основе рабочего check_tables.py)
"""

import os
from dotenv import load_dotenv
# ==========================================
# 🌍 НАСТРОЙКА ПРОКСИ ИЗ .ENV
# ==========================================
# Загружаем переменные из файла .env
load_dotenv()

# Получаем значение PROXY_URL
proxy_url = os.getenv("PROXY_URL")

if proxy_url:
    print(f"⚙️  Найдена настройка прокси в .env")
    # Применяем прокси
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    print(f"   ✅ Прокси активирован")
else:
    print("ℹ️  Прокси не задан (файл .env или переменная PROXY_URL отсутствуют)")

# ==========================================
import json
import csv
from pathlib import Path


OUTPUT_DIR = Path("output")
TABLES_DIR = OUTPUT_DIR / "tables_csv"


def extract_tables_from_json(json_file):
    """
    Извлекает таблицы из JSON файла (РАБОЧАЯ ВЕРСИЯ)
    
    Возвращает:
        list: Список таблиц
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tables = []
    
    # Проверяем main-text (основной контент)
    main_text = data.get('main-text', [])
    
    # ВАЖНО: main_text может быть списком строк или списком dict
    if isinstance(main_text, list):
        for item in main_text:
            # Проверяем, что это dict (а не строка!)
            if isinstance(item, dict) and item.get('type') == 'table':
                tables.append(item)
    
    # Также проверяем tables (альтернативный ключ)
    if 'tables' in data and isinstance(data['tables'], list):
        for item in data['tables']:
            if isinstance(item, dict):
                tables.append(item)
    
    # Проверяем body (ещё одна структура)
    body = data.get('body', [])
    if isinstance(body, list):
        for item in body:
            if isinstance(item, dict) and item.get('type') == 'table':
                tables.append(item)
    
    return tables


def table_to_csv(table_data, output_file):
    """
    Конвертирует таблицу из JSON в CSV
    
    Параметры:
        table_data: Данные таблицы из JSON
        output_file: Путь для сохранения CSV
        
    Возвращает:
        bool: True если успешно, False если ошибка
    """
    try:
        # Проверяем наличие данных
        if 'data' not in table_data:
            print(f"   ⚠️  Таблица без данных")
            return False
        
        table_cells = table_data['data'].get('table_cells', [])
        
        if not table_cells:
            print(f"   ⚠️  Пустая таблица")
            return False
        
        # Определяем размер таблицы
        max_row = 0
        max_col = 0
        
        for cell in table_cells:
            end_row = cell.get('end_row_offset_idx', 0)
            end_col = cell.get('end_col_offset_idx', 0)
            
            if end_row > max_row:
                max_row = end_row
            if end_col > max_col:
                max_col = end_col
        
        # Создаём пустую матрицу
        grid = [['' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
        
        # Заполняем ячейки
        for cell in table_cells:
            start_row = cell.get('start_row_offset_idx', 0)
            start_col = cell.get('start_col_offset_idx', 0)
            text = cell.get('text', '').strip()
            
            # Проверяем границы
            if start_row <= max_row and start_col <= max_col:
                grid[start_row][start_col] = text
        
        # Записываем в CSV
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(grid)
        
        print(f"   ✅ {output_file.name} ({max_row+1}×{max_col+1})")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка при сохранении: {e}")
        return False


def process_document(json_file):
    """
    Обрабатывает один документ: извлекает все таблицы в CSV
    """
    print(f"📄 {json_file.name}")
    
    # Извлекаем таблицы
    tables = extract_tables_from_json(json_file)
    
    if not tables:
        print(f"   ⚠️  Таблиц не найдено")
        print()
        return 0
    
    print(f"   📊 Найдено таблиц: {len(tables)}")
    
    # Создаём папку для таблиц этого документа
    doc_name = json_file.stem
    doc_tables_dir = TABLES_DIR / doc_name
    doc_tables_dir.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем каждую таблицу
    success_count = 0
    for i, table in enumerate(tables, 1):
        csv_file = doc_tables_dir / f"table_{i}.csv"
        if table_to_csv(table, csv_file):
            success_count += 1
    
    print(f"   ✅ Сохранено: {success_count}/{len(tables)}")
    print()
    
    return success_count


def main():
    print()
    print("=" * 70)
    print("📊 ИЗВЛЕЧЕНИЕ ТАБЛИЦ В CSV")
    print("=" * 70)
    print()
    
    if not OUTPUT_DIR.exists():
        print(f"❌ Папка не найдена: {OUTPUT_DIR}")
        return
    
    # Создаём папку для CSV
    TABLES_DIR.mkdir(exist_ok=True)
    
    # Получаем JSON файлы
    json_files = list(OUTPUT_DIR.glob("*.json"))
    json_files = [f for f in json_files if not f.name.endswith('_tables.json')]
    json_files = sorted(json_files)
    
    if not json_files:
        print("❌ JSON файлы не найдены")
        return
    
    print(f"📂 Найдено файлов: {len(json_files)}")
    print()
    
    # Обрабатываем каждый документ
    total_saved = 0
    for json_file in json_files:
        total_saved += process_document(json_file)
    
    print("=" * 70)
    print(f"✅ ГОТОВО! Извлечено таблиц: {total_saved}")
    print(f"📂 Папка: {TABLES_DIR.absolute()}")
    print("=" * 70)
    print()
    print("💡 Откройте в проводнике:")
    print(f"   explorer {TABLES_DIR}")
    print()


if __name__ == "__main__":
    main()

"""
Инспектор структуры JSON документов Docling
"""

import json
from pathlib import Path


OUTPUT_DIR = Path("output")


def inspect_json_structure(json_file, max_depth=3):
    """
    Показывает структуру JSON файла
    
    Параметры:
        json_file: Путь к JSON
        max_depth: Максимальная глубина отображения
    """
    print(f"📄 {json_file.name}")
    print("=" * 70)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    def show_structure(obj, indent=0, depth=0, key_name="root"):
        """Рекурсивно показывает структуру"""
        if depth > max_depth:
            return
        
        prefix = "  " * indent
        
        if isinstance(obj, dict):
            print(f"{prefix}{key_name}: {{dict}} ({len(obj)} ключей)")
            
            for key, value in list(obj.items())[:5]:  # Показываем первые 5 ключей
                show_structure(value, indent + 1, depth + 1, key)
            
            if len(obj) > 5:
                print(f"{prefix}  ... ещё {len(obj) - 5} ключей")
        
        elif isinstance(obj, list):
            print(f"{prefix}{key_name}: [list] ({len(obj)} элементов)")
            
            if obj and len(obj) > 0:
                print(f"{prefix}  Пример элемента [0]:")
                show_structure(obj[0], indent + 1, depth + 1, "[0]")
        
        elif isinstance(obj, str):
            preview = obj[:50] + "..." if len(obj) > 50 else obj
            print(f"{prefix}{key_name}: \"{preview}\"")
        
        else:
            print(f"{prefix}{key_name}: {type(obj).__name__} = {obj}")
    
    show_structure(data)
    print()


def main():
    print()
    print("=" * 70)
    print("🔬 ИНСПЕКТОР СТРУКТУРЫ JSON")
    print("=" * 70)
    print()
    
    if not OUTPUT_DIR.exists():
        print(f"❌ Папка не найдена: {OUTPUT_DIR}")
        return
    
    json_files = list(OUTPUT_DIR.glob("*.json"))
    json_files = [f for f in json_files if not f.name.endswith('_tables.json')]
    
    if not json_files:
        print("❌ JSON файлы не найдены")
        return
    
    # Показываем структуру первого файла детально
    print("📊 Детальная структура первого файла:")
    print()
    inspect_json_structure(json_files[0], max_depth=4)
    
    print("=" * 70)
    print("💡 Используйте эту информацию для понимания структуры")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

"""
Анализ структуры JSON документов
"""

import json
from pathlib import Path
from collections import Counter


OUTPUT_DIR = Path("output")


def analyze_document_structure(json_file):
    """Анализирует структуру документа из JSON"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📄 {json_file.name}")
    print("   " + "=" * 60)
    
    # Общая информация
    if 'name' in data:
        print(f"   Название: {data['name']}")
    
    # Статистика по типам элементов
    element_types = [item.get('type', 'unknown') 
                     for item in data.get('main_text', [])]
    type_counts = Counter(element_types)
    
    print(f"   📊 Статистика элементов:")
    for elem_type, count in type_counts.most_common():
        print(f"      • {elem_type}: {count}")
    
    # Метаданные
    if 'metadata' in data:
        meta = data['metadata']
        if 'num_pages' in meta:
            print(f"   📄 Страниц: {meta['num_pages']}")
    
    # Текстовая статистика
    all_text = ' '.join([item.get('text', '') 
                         for item in data.get('main_text', [])])
    words = len(all_text.split())
    chars = len(all_text)
    
    print(f"   📝 Слов: {words}")
    print(f"   📝 Символов: {chars}")
    
    print()


def main():
    print()
    print("=" * 70)
    print("🔬 АНАЛИЗ СТРУКТУРЫ ДОКУМЕНТОВ")
    print("=" * 70)
    print()
    
    json_files = list(OUTPUT_DIR.glob("*.json"))
    json_files = [f for f in json_files if not f.name.endswith('_tables.json')]
    json_files = sorted(json_files)
    
    if not json_files:
        print("❌ JSON файлы не найдены")
        return
    
    for json_file in json_files:
        analyze_document_structure(json_file)
    
    print("=" * 70)
    print(f"✅ Проанализировано файлов: {len(json_files)}")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

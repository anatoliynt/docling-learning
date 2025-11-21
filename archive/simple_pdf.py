"""
Простая конвертация PDF без прокси
Работает быстро, так как модели уже в кэше
"""

from docling.document_converter import DocumentConverter
import time

# ====================================================================
# ФУНКЦИЯ: Конвертация PDF
# ====================================================================

def convert_pdf_simple(pdf_path):
    """
    Конвертирует PDF в Markdown без прокси
    
    Параметры:
        pdf_path (str): Путь к PDF файлу
    """
    print("=" * 60)
    print("🔄 КОНВЕРТАЦИЯ PDF")
    print("=" * 60)
    print(f"📄 Файл: {pdf_path}")
    print("⏳ Загружаем модели в память...")
    print()
    
    # Засекаем время
    start_time = time.time()
    
    try:
        # Создаём конвертер
        # Модели загрузятся из кэша (с вчерашнего дня)
        converter = DocumentConverter()
        
        print("✅ Модели загружены!")
        print("🔄 Обрабатываем документ...")
        print()
        
        # Конвертируем
        result = converter.convert(pdf_path)
        doc = result.document
        
        # Сохраняем результат
        output_file = "output_simple.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(doc.export_to_markdown())
        
        # Считаем время
        elapsed_time = time.time() - start_time
        
        print("=" * 60)
        print("✅ УСПЕХ!")
        print("=" * 60)
        print(f"📄 Результат: {output_file}")
        print(f"📊 Страниц: {len(doc.pages)}")
        print(f"⏱️  Время: {elapsed_time:.2f} секунд")
        print()
        
        # Показываем первые 500 символов
        markdown = doc.export_to_markdown()
        print("=== ПРЕВЬЮ (первые 500 символов) ===")
        print(markdown[:500])
        print("...")
        print()
        
        return True
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print()
        print("=" * 60)
        print("❌ ОШИБКА")
        print("=" * 60)
        print(f"Описание: {e}")
        print(f"Время до ошибки: {elapsed_time:.2f} секунд")
        print()
        return False


# ====================================================================
# ЗАПУСК ПРОГРАММЫ
# ====================================================================

if __name__ == "__main__":
    # Конвертируем файл
    convert_pdf_simple("test.pdf")

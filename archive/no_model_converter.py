# Импортируем необходимые классы
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

# ====================================================================
# ФУНКЦИЯ: Создание конвертера без сложных моделей
# ====================================================================
# do_ocr=False - отключаем оптическое распознавание символов
# do_table_structure=False - отключаем анализ таблиц
# generate_page_images=False - не генерируем изображения страниц
# generate_picture_images=False - не извлекаем картинки
# ====================================================================

def create_simple_converter():
    """
    Создаёт конвертер без загрузки моделей из интернета.
    Работает только с текстовыми PDF (не сканированными).
    """
    # Настраиваем опции обработки PDF
    pipeline_options = PdfPipelineOptions(
        do_ocr=False,                    # НЕ использовать OCR
        do_table_structure=False,        # НЕ анализировать таблицы
        generate_page_images=False,      # НЕ генерировать изображения
        generate_picture_images=False,   # НЕ извлекать картинки
    )
    
    # Создаём конвертер с простым backend (без моделей)
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend  # Простой парсер без AI
            )
        }
    )
    
    return converter


# ====================================================================
# ОСНОВНАЯ ПРОГРАММА
# ====================================================================

# Путь к вашему локальному PDF файлу
# ИНСТРУКЦИЯ: Положите PDF в папку C:\VScode\ и укажите имя ниже
source = "Даниил Солнечный распил схема.pdf"  # Измените на имя вашего файла!

print(f"🔄 Начинаем конвертацию файла: {source}")
print("⚠️  Внимание: работает только с текстовыми PDF (не сканами)")
print()

# Создаём конвертер
converter = create_simple_converter()

try:
    # Конвертируем документ
    result = converter.convert(source)
    doc = result.document
    
    # Экспортируем в Markdown
    markdown_content = doc.export_to_markdown()
    
    # Сохраняем результат в файл
    output_file = "output_simple.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print("✅ УСПЕХ!")
    print(f"📄 Результат сохранён в файл: {output_file}")
    print(f"📊 Обработано {len(doc.pages)} страниц")
    print()
    print("=== ПЕРВЫЕ 500 СИМВОЛОВ ===")
    print(markdown_content[:500])
    print("...")
    
except FileNotFoundError:
    print(f"❌ ОШИБКА: Файл '{source}' не найден!")
    print(f"   Положите PDF файл в папку: C:\\VScode\\")
    print(f"   И измените переменную source в коде")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    print()
    print("💡 Возможные причины:")
    print("   - Файл повреждён")
    print("   - PDF является сканом (нужен OCR, но он отключён)")
    print("   - Неподдерживаемый формат PDF")

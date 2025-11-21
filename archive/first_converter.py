# Импортируем необходимые классы
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Настраиваем упрощённый режим обработки PDF
# do_ocr=False - отключаем OCR для ускорения
# do_table_structure=False - отключаем распознавание таблиц
pipeline_options = PdfPipelineOptions(
    do_ocr=False,              # Отключаем OCR
    do_table_structure=False    # Отключаем анализ таблиц
)

# Создаём конвертер с упрощёнными настройками
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

# Источник документа
source = "Даниил Солнечный распил схема.pdf"

# Конвертируем документ
print("Начинаем конвертацию...")
result = converter.convert(source)
doc = result.document

# Экспортируем результат
print("\n=== РЕЗУЛЬТАТ КОНВЕРТАЦИИ ===\n")
print(doc.export_to_markdown())

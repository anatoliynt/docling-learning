"""
Демонстрация настроек Pipeline (БРОНЕБОЙНАЯ ВЕРСИЯ)
Отключаем Xet, Symlinks и используем PyPdfium2
Этап 3.2
"""
import os
import time
from pathlib import Path

# === БЛОК НАСТРОЕК ОКРУЖЕНИЯ (Вставлять ДО любых импортов docling) ===
# 1. Отключаем Xet Storage (глючит на некоторых сетях)
os.environ["HF_HUB_DISABLE_XET"] = "1"
# 2. Отключаем экспериментальную передачу файлов
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
# 3. Отключаем предупреждение про симлинки в Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# 4. Увеличиваем таймауты скачивания (чтобы не рвалось на медленном инете)
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "300"
os.environ["HF_HUB_ETAG_TIMEOUT"] = "300"
# ======================================================================

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

# Пути
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output" / "custom_settings"

def run_converter_with_settings(file_path, setting_name, pipeline_options):
    print(f"\n⚙️  Запуск режима: {setting_name}")
    
    # Используем PyPdfium2Backend для стабильности на Windows
    format_options = {
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
            backend=PyPdfiumDocumentBackend 
        )
    }
    
    try:
        # Создаем конвертер
        converter = DocumentConverter(format_options=format_options)
        
        start_time = time.time()
        # Конвертация
        result = converter.convert(str(file_path))
        elapsed = time.time() - start_time
        
        # Сохранение
        output_path = OUTPUT_DIR / f"{file_path.stem}_{setting_name}.md"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.document.export_to_markdown())
            
        print(f"   ✅ Готово за {elapsed:.2f} сек")
        print(f"   📄 Сохранено: {output_path.name}")
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def main():
    # Ищем PDF
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("❌ Нет PDF файлов в папке input!")
        return
    
    test_file = pdf_files[0]
    print(f"🧪 Тестируем на файле: {test_file.name}")

    # СЦЕНАРИЙ 1: Быстрый (Только текст)
    print("\n--- ТЕСТ 1: БЕЗ OCR ---")
    fast_options = PdfPipelineOptions(
        do_ocr=False,
        do_table_structure=False
    )
    run_converter_with_settings(test_file, "fast_no_ocr", fast_options)

    # СЦЕНАРИЙ 2: Полный (OCR + Таблицы)
    print("\n--- ТЕСТ 2: ПОЛНЫЙ OCR ---")
    heavy_options = PdfPipelineOptions(
        do_ocr=True,
        do_table_structure=True,
        table_structure_options={"mode": TableFormerMode.ACCURATE}
    )
    run_converter_with_settings(test_file, "full_ocr", heavy_options)

if __name__ == "__main__":
    main()

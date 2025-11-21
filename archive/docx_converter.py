from docling.document_converter import DocumentConverter

converter = DocumentConverter()

# Для DOCX не нужны модели!
source = "document.docx"  
result = converter.convert(source)

with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())

print("✅ Готово!")

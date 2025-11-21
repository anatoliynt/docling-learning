import os
import urllib3

# ====================================================================
# НАСТРОЙКА HTTPS ПРОКСИ (исправленная версия)
# ====================================================================

# Ваши данные прокси (ЗАМЕНИТЕ на реальные!)
PROXY_HOST = "168.80.203.70"       # IP или домен прокси
PROXY_PORT = "8000"                # Порт прокси
PROXY_USER = "9u4bcR"               # Логин (замените!)
PROXY_PASS = "gBdhq7"                # Пароль (замените!)

# ДЛЯ HTTPS ПРОКСИ используем https:// в URL
proxy_url_https = f"https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxy_url_http = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

# Устанавливаем переменные окружения
# Для HTTPS прокси часто нужно указывать https:// протокол
os.environ['HTTP_PROXY'] = proxy_url_https   # HTTPS прокси для HTTP
os.environ['HTTPS_PROXY'] = proxy_url_https  # HTTPS прокси для HTTPS
os.environ['http_proxy'] = proxy_url_https
os.environ['https_proxy'] = proxy_url_https

# Отключаем проверку SSL сертификата прокси
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(f"🌐 HTTPS Прокси настроен: {PROXY_HOST}:{PROXY_PORT}")
print(f"👤 Пользователь: {PROXY_USER}")
print()

# ====================================================================
# ИМПОРТИРУЕМ DOCLING ПОСЛЕ НАСТРОЙКИ
# ====================================================================

from docling.document_converter import DocumentConverter

# Конвертация
source = "test.pdf"

print(f"🔄 Конвертируем через HTTPS прокси: {source}")
print()

try:
    converter = DocumentConverter()
    result = converter.convert(source)
    
    with open("output_https_proxy.md", "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())
    
    print("✅ УСПЕХ! Файл: output_https_proxy.md")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")

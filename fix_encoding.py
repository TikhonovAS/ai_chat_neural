# fix_encoding.py — массовая конвертация в UTF-8 без BOM
import sys
from pathlib import Path

# Расширения, которые нужно конвертировать
TEXT_EXTENSIONS = {'.py', '.toml', '.yml', '.md', '.json', '.txt', '.cfg', '.ini'}


def fix_file(file_path: Path) -> bool:
    """Читает файл, определяет кодировку, сохраняет в UTF-8 без BOM"""
    try:
        # 1. Читаем как байты
        raw = file_path.read_bytes()

        # 2. Пробуем декодировать в порядке вероятности
        text = None
        for encoding in ['utf-8-sig', 'utf-8', 'cp1251', 'utf-16']:
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue

        if text is None:
            print(f"⚠️  Пропуск (бинарный/неизвестный): {file_path.name}")
            return False

        # 3. Записываем обратно в чистый UTF-8 (Python 3 пишет без BOM по умолчанию)
        file_path.write_text(text, encoding='utf-8')
        print(f"✅ Конвертировано: {file_path.relative_to(Path.cwd())}")
        return True

    except Exception as e:
        print(f"❌ Ошибка {file_path.name}: {e}")
        return False


if __name__ == "__main__":
    project_root = Path.cwd()
    converted = 0

    print(f"🔍 Поиск файлов в {project_root}...")
    for ext in TEXT_EXTENSIONS:
        for file_path in project_root.rglob(f"*{ext}"):
            # Пропускаем виртуальные окружения и кэш
            if '.venv' in file_path.parts or '__pycache__' in file_path.parts or '.git' in file_path.parts:
                continue
            if fix_file(file_path):
                converted += 1

    print(f"\n🎉 Готово! Конвертировано файлов: {converted}")
    print("💡 Не забудь удалить этот скрипт после запуска: Remove-Item fix_encoding.py")
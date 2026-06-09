import json
from pathlib import Path
from datetime import datetime


class ChatHistory:
    """
    Класс для хранения диалога.
    Поддерживает: добавление сообщений, сохранение в JSON, загрузку
    """

    def __init__(self, filepath="history.json"):
        self.filepath = Path(filepath)
        self.messages = []
        self._load()

    def add_message(self, role, content):
        """Добавляет сообщение в историю и сразу сохранияет на диск"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self._save()

    def get_context(self, max_messages=10):
        """Возвращает последние N сообщений для отправки в API"""
        return self.messages[-max_messages:]

    def clear(self):
        """Очищает историю"""
        self.messages = []
        self._save()

    def _save(self):
        """Внутренний метод: сохраняет историю в JSON-файл"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def _load(self):
        """Внутренний метод: загружает историю из файла, если он есть"""
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:  # Файл пустой
                        self.messages = []
                        return
                    self.messages = json.loads(content)

            except json.JSONDecodeError:
                # Если файл поврежден или пустой, начинаем с нуля
                print("history.json поврежден. Начинаю новую историю.")
                self.messages = []
                self._save()  # перезаписываем файл корректным пустым списком

            except Exception as e:
                # Любой другой фарс-мажор (права доступа, сбой диска)
                print(f"Ошибка загрузки истории: {e}. Начинаю с нуля.")
                self.messages = []

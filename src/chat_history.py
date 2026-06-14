import json
import logging
from pathlib import Path
from src.config import Settings

logger = logging.getLogger(__name__)


class ChatHistory:
    """Управление историей диалога: сохранение, загрузка, ограничение контекста."""

    def __init__(self, file_path: str = Settings.HISTORY_FILE, max_messages: int = 10):
        self.file_path = Path(file_path)
        self.max_messages = max_messages
        self.messages: list[dict] = []
        self._load()

    def _load(self) -> None:
        """Загружает историю из файла. При ошибке начинает с пустого списка."""
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.messages = json.load(f)
                logger.info(f"📂 Загружено {len(self.messages)} сообщений из истории")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"⚠️ История повреждена или недоступна: {e}. Начинаем заново.")
            self.messages = []

    def save(self) -> None:
        """Сохраняет историю в JSON."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"❌ Ошибка сохранения истории: {e}")

    def add_message(self, role: str, content: str) -> None:
        """Добавляет сообщение и сразу сохраняет."""
        self.messages.append({"role": role, "content": content})
        self.save()

    def get_context(self) -> list[dict]:
        """Возвращает последние N сообщений для контекста ИИ."""
        return self.messages[-self.max_messages:]

    def clear(self) -> None:
        """Очищает историю и файл."""
        self.messages.clear()
        if self.file_path.exists():
            self.file_path.unlink()
        logger.info("🗑 История очищена")
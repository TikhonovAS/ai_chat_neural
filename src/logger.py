import logging
import sys
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_file: str = "bot.log", level: int = logging.DEBUG):
    """
  Настраивает систему логирования для всего проекта.
  Создаёт папку logs/, настраивает запись в файл и вывод в консоль.
  """
    # 1. Создаём директорию, если её нет
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    full_path = Path(log_dir) / log_file

    # 2. Получаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # ✅ Простой и надёжный формат (без сложных спецификаторов)
    # Все поля имеют суффиксы: %(asctime)s, %(levelname)s, %(name)s, %(lineno)d, %(message)s
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. Обработчик 1: ФАЙЛ (пишет ВСЁ, включая DEBUG)
    file_handler = logging.FileHandler(full_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 4. Обработчик 2: КОНСОЛЬ (показывает только INFO и выше)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 5. Гасим шум от requests/urllib3
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # ✅ Явно логгируем успешную настройку
    root_logger.info("🔧 Логирование настроено: файл=%s, уровень=%s", full_path, logging.getLevelName(level))

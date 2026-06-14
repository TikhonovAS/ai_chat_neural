import logging
from pathlib import Path
from src.config import Settings


def setup_logging() -> None:
    """
    Настраивает систему логирования для всего проекта.
    - Устанавливает уровень (DEBUG в dev, INFO в prod)
    - Подключает вывод в консоль и файл
    - Фильтрует шум от сторонних библиотек
    """
    # Гарантируем, что директория для логов существует
    log_path = Path(Settings.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Базовая конфигурация корневого логгера
    logging.basicConfig(
        level=logging.DEBUG if Settings.DEBUG_MODE else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),  # Вывод в терминал
            logging.FileHandler(log_path, encoding="utf-8", mode="a")  # Дописывание в файл
        ]
    )

    # 📉 Убираем лишний шум от HTTP-клиентов (requests/urllib3/httpx)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("🔧 Логирование настроено: файл=%s, уровень=%s",
                 Settings.LOG_FILE, "DEBUG" if Settings.DEBUG_MODE else "INFO")
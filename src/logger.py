import logging
import sys
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_file: str = "bot.log", level: int = logging.DEBUG):
    """
  РќР°СЃС‚СЂР°РёРІР°РµС‚ СЃРёСЃС‚РµРјСѓ Р»РѕРіРёСЂРѕРІР°РЅРёСЏ РґР»СЏ РІСЃРµРіРѕ РїСЂРѕРµРєС‚Р°.
  РЎРѕР·РґР°С‘С‚ РїР°РїРєСѓ logs/, РЅР°СЃС‚СЂР°РёРІР°РµС‚ Р·Р°РїРёСЃСЊ РІ С„Р°Р№Р» Рё РІС‹РІРѕРґ РІ РєРѕРЅСЃРѕР»СЊ.
  """
    # 1. РЎРѕР·РґР°С‘Рј РґРёСЂРµРєС‚РѕСЂРёСЋ, РµСЃР»Рё РµС‘ РЅРµС‚
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    full_path = Path(log_dir) / log_file

    # 2. РџРѕР»СѓС‡Р°РµРј РєРѕСЂРЅРµРІРѕР№ Р»РѕРіРіРµСЂ
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # вњ… РџСЂРѕСЃС‚РѕР№ Рё РЅР°РґС‘Р¶РЅС‹Р№ С„РѕСЂРјР°С‚ (Р±РµР· СЃР»РѕР¶РЅС‹С… СЃРїРµС†РёС„РёРєР°С‚РѕСЂРѕРІ)
    # Р’СЃРµ РїРѕР»СЏ РёРјРµСЋС‚ СЃСѓС„С„РёРєСЃС‹: %(asctime)s, %(levelname)s, %(name)s, %(lineno)d, %(message)s
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. РћР±СЂР°Р±РѕС‚С‡РёРє 1: Р¤РђР™Р› (РїРёС€РµС‚ Р’РЎРЃ, РІРєР»СЋС‡Р°СЏ DEBUG)
    file_handler = logging.FileHandler(full_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 4. РћР±СЂР°Р±РѕС‚С‡РёРє 2: РљРћРќРЎРћР›Р¬ (РїРѕРєР°Р·С‹РІР°РµС‚ С‚РѕР»СЊРєРѕ INFO Рё РІС‹С€Рµ)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 5. Р“Р°СЃРёРј С€СѓРј РѕС‚ requests/urllib3
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # вњ… РЇРІРЅРѕ Р»РѕРіРіРёСЂСѓРµРј СѓСЃРїРµС€РЅСѓСЋ РЅР°СЃС‚СЂРѕР№РєСѓ
    root_logger.info("рџ”§ Р›РѕРіРёСЂРѕРІР°РЅРёРµ РЅР°СЃС‚СЂРѕРµРЅРѕ: С„Р°Р№Р»=%s, СѓСЂРѕРІРµРЅСЊ=%s", full_path, logging.getLevelName(level))

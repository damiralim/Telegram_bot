from loguru import logger
from typing import Optional

''' Проверка названия города '''

def is_alpha(cityname: str) -> Optional[str]:
    for sym in cityname:
        if sym != '-' and not sym.isalpha():
            return 'Вы ввели название города, содержащее символы либо числа'

''' Проверка числового параметра '''

def is_correct(num: str) -> Optional[bool]:
    try:
        int(num)
    except ValueError as exc:
        logger.exception(f'Вызвано исключение: {exc}')
        return 'Вы ввели букву/символ вместо числа, либо оно превышает установленный лимит'





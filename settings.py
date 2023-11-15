from dotenv import load_dotenv
import os

load_dotenv('.env')

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRM_TOKEN = os.getenv("CRM_TOKEN")
CRM_URL = os.getenv("CRM_URL")

# Разметка парсинга текстов в боте. Применяется ко всему проекту.
# https://docs.aiogram.dev/en/dev-3.x/api/enums/parse_mode.html#
PARSE_MODE = 'HTML'

# Статус заказ “Доставка Казань“
STATUS_DELIVERY_KAZAN = 'delivery-kazan'
STATUS_ORDER_COMPLETE = 'complete'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # . False - существующие логгеры будут работать.
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {  # Подробный формат
            'format':
                '{asctime} {levelname} В модуле "{name}" {module} {process} {thread} в строке {lineno:03d}: {message}',
            'style': '{',
        },
        'standard': {
            'format': '{asctime} {levelname:<8} В модуле {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            # 'stream': sys.stdout, # Не меняет вывод
        },
        # 'file': {
        #     'formatter': 'standard',
        #     'class': 'logging.FileHandler',
        #     'level': 'DEBUG',
        #     'filename': './log/log.log'
        #     # Можно добавить 'mode': 'w'
        # },
        'zip_file': {
            'formatter': 'standard',
            'class': 'loger.ZipTimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': './log/log.log',
            # 'suffix': "%Y-%m-%d"
            # 'when': "D",
            # 'interval': 1,
            # 'backupCount': 7,
            # 'encoding': 'utf-8',
            # 'delay': True,
        }
    },
    'loggers': {
        # 'aiogram': {
        #     'handlers': ['console', 'zip_file'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'loger': {
            'handlers': ['console', 'zip_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

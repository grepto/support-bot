import os
import logging.config
import argparse
from dotenv import load_dotenv

from tg_bot import start_bot as tg_bot
from vk_bot import bot as vk_bot
from train_bot import train_bot


load_dotenv()
LOG_LEVEL = os.getenv('LOG_LEVEL')
QUESTIONS_FILE = os.getenv('QUESTIONS_FILE')

parser = argparse.ArgumentParser(description='Support bot')
parser.add_argument('-startbot', action='store', dest='bot', choices=['tg', 'vk'], help='Starting TG or VK bot')
parser.add_argument('-train', action='store_true', dest='is_train_mode', help='Key for start training')
parser.add_argument('--forse', action='store_true', dest='is_rewrite_answers',
                    help='If this key is passed, the answers in Dialogflow will be overwritten by the answers from the file')
args = parser.parse_args()

if __name__ == '__main__':
    log_config = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'base_Formatter',
                'level': LOG_LEVEL,
            },
            'telegram': {
                'class': 'log_handlers.TelegramHandler',
                'formatter': 'tg_Formatter',
                'level': 'INFO',
            }
        },
        'loggers': {
            'tg_bot': {
                'handlers': ['console', 'telegram'],
                'level': LOG_LEVEL,
            },
            'vk_bot': {
                'handlers': ['console', 'telegram'],
                'level': LOG_LEVEL,
            },
            'JobQueue': {
                'handlers': ['console', 'telegram'],
                'level': LOG_LEVEL,
            },
            'train_bot': {
                'handlers': ['console'],
                'level': LOG_LEVEL,
            },
        },
        'formatters': {
            'base_Formatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'tg_Formatter': {
                'format': '%(asctime)s\n%(name)s\n%(levelname)s\n%(message)s',
            },
        }
    }
    logging.config.dictConfig(log_config)
    if args.bot == 'tg':
        tg_bot()
    elif args.bot == 'vk':
        vk_bot()

    if args.is_train_mode:
        train_bot(QUESTIONS_FILE, args.is_rewrite_answers)

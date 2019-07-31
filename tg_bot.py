import os
import logging

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialog import get_dialog_response

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')

logger = logging.getLogger('tg_bot')


def send_wellcome_message(bot, update):
    update.message.reply_text('Здравствуйте\nЧто вас интересует?')


def send_help_message(bot, update):
    update.message.reply_text(
        'Бот ответит на вопросы по работа с вашим аккаунтом и проконсультирует по поводу устройства на работу')


def send_echo(bot, update):
    update.message.reply_text(update.message.text)


def send_dialog_answer(bot, update):
    response = get_dialog_response(update.message.chat_id, update.message.text)
    update.message.reply_text(response['response_text'])


def send_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_uppercased_echo(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def start_bot():
    try:
        logger.info(f'TG bot started')
        updater = Updater(TG_TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", send_wellcome_message))
        dp.add_handler(CommandHandler("help", send_help_message))
        dp.add_handler(CommandHandler("caps", get_uppercased_echo, pass_args=True))

        dp.add_handler(MessageHandler(Filters.text, send_dialog_answer))

        dp.add_error_handler(send_error)

        updater.start_polling()

        updater.idle()
    except Updater as err:
        logger.error(err)


if __name__ == '__main__':
    start_bot()

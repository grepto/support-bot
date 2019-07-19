import os
import logging

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialog import get_dialog_response

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')

logger = logging.getLogger('tg_bot')


def start(bot, update):
    update.message.reply_text('Здравствуйте\nЧто вас интересует?')


def help(bot, update):
    update.message.reply_text(
        'Бот ответит на вопросы по работа с вашим аккаунтом и проконсультирует по поводу устройства на работу')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def dialog(bot, update):
    response = get_dialog_response(update.message.chat_id, update.message.text)
    update.message.reply_text(response['response_text'])


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def bot():
    try:
        logger.info(f'TG bot started')
        updater = Updater(TG_TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("caps", caps, pass_args=True))

        dp.add_handler(MessageHandler(Filters.text, dialog))

        dp.add_error_handler(error)

        updater.start_polling()

        updater.idle()
    except Updater as err:
        logger.error(err)


if __name__ == '__main__':
    bot()

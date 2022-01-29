import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#Initialization




# Enable logging info

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    # Probably will ask for the user if they want to subscribe to the bot
    update.message.reply_text('Hi! Would you like to subscribe to the bot?')
    questions = ['Subscribe?',
                 'Help?',
                 'Data?',
                 'Stop?',
                 ]
    buttons = []
    for question in questions:
        buttons.append(InlineKeyboardButton(question, callback_data=question))
    reply_markup = InlineKeyboardMarkup(menu_builder(buttons, n_cols=1))  # 1 column
    context.bot.send_message(chat_id=update.message.chat_id, text='Choose an option', reply_markup=reply_markup)


def menu_builder(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append()
    return menu


def stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bye!')
    update.stop()


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def data(update: Update, context: CallbackContext) -> None:
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text='Data')


def main() -> None:
    bot_token = '2139077813:AAGJorjPQsfSw7s7-88IdLVe2sFOd_ZhHqc'
    updater = Updater('2139077813:AAGJorjPQsfSw7s7-88IdLVe2sFOd_ZhHqc', use_context=True)
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# standard
import logging
import os

# third party
from environs import Env
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler
import django

# local

# code area
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetup_management.settings')
django.setup()

from manager.models import Event

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

EVENT = 0


def start(update, context):
    text = 'Добро пожаловать!'

    inline_keyboard_buttons = [
        [InlineKeyboardButton(event.title, callback_data=event.id)]
        for event in Event.objects.all()
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard_buttons)

    # buttons = [
    #     [InlineKeyboardButton('hi', callback_data='hi')]
    # ]
    # keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=inline_keyboard)

    return EVENT


def handle_event(update, context):
    pass


def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={EVENT: [CallbackQueryHandler(handle_event)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

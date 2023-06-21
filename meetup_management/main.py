import os

from environs import Env
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetup_management.settings')
django.setup()

from manager.models import Event


def get_updater():
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    return Updater(token=tg_bot_token)


def start(update, context):
    inline_keyboard_buttons = [
        [InlineKeyboardButton(event.title, callback_data=event.id)]
        for event in Event.objects.all()
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard_buttons)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберете мероприятие!",
        reply_markup=inline_keyboard,
    )


def button_tap(update, context):
    pass


if __name__ == '__main__':
    updater = get_updater()
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    updater.start_polling()

    updater.idle()

    # print(Event.objects.create())

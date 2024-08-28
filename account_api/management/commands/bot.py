from django.core.management.base import BaseCommand
from main_settings import settings

from telebot import TeleBot


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_TOKEN, threaded=False)

def send_telegram_message(chat_id, message: str):
    bot.send_message(chat_id=chat_id, text=message)

class Command(BaseCommand):
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()				# Загрузка обработчиков
        bot.infinity_polling()
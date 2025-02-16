from telegram.ext import Application
from handlers.start import get_start_handlers
from handlers.department import get_department_handlers, get_admin_reply_handler

import logging
from handlers.admin import get_admin_handlers
  # Импортируем обработчик расписания отделов

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8065077573:AAE5XGOJHo7PoolwlujJpDZaJYlSuK_PeWk"

def main():
    application = Application.builder().token(TOKEN).build()

    # Сначала регистрируем ConversationHandler (он должен иметь приоритет)
    application.add_handler(get_department_handlers())  # Диалог "Задать вопрос"
    application.add_handler(get_admin_reply_handler())  # Ответы админов

    # Затем общие обработчики (чтобы не перехватывали сообщения)
    application.add_handlers(get_start_handlers())      # Главное меню

    application.add_handlers(get_admin_handlers())

    # Добавляем обработчик для расписания отделов


    logger.info("Бот запущен.")
    application.run_polling()

if __name__ == "__main__":
    main()
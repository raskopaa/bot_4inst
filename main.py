from telegram.ext import Application
from handlers.start import get_start_handlers
from handlers.department import get_department_handlers, get_admin_reply_handler
from handlers.career_test import get_career_test_handler
import logging
from handlers.admin import get_admin_handlers
  # Импортируем обработчик расписания отделов

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8065077573:AAE5XGOJHo7PoolwlujJpDZaJYlSuK_PeWk"

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(get_career_test_handler())
    # Добавляем обработчики
    application.add_handler(get_start_handlers())  # Главное меню (с выбором роли)
    application.add_handler(get_department_handlers())  # Диалог "Задать вопрос"
    application.add_handler(get_admin_reply_handler())  # Ответы админов

    # get_admin_handlers() возвращает список, добавляем их по очереди
    for handler in get_admin_handlers():
        application.add_handler(handler)

    logger.info("Бот запущен.")
    application.run_polling()


if __name__ == "__main__":
    main()

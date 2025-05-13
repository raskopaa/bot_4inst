from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
)
import json
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERS_FILE = "users.json"
CHOOSING_ROLE = 1  # Этап диалога выбора роли


# Функция загрузки пользователей
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data  # ✅ Если файл содержит словарь, возвращаем его
            else:
                return {}  # ❌ Если вдруг список или что-то другое, исправляем
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # ✅ Если файл отсутствует или пустой, возвращаем пустой словарь
# Функция сохранения пользователей
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


# Функция добавления пользователя
def add_user(user_id, role):
    users = load_users()
    users[str(user_id)] = role
    save_users(users)


async def start(update: Update, context: CallbackContext):
    """Запросить у пользователя, кто он: студент или абитуриент"""
    logger.info(f"Пользователь {update.message.from_user.id} запустил бота.")

    keyboard = [["Студент", "Абитуриент"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Выберите, кто вы: студент или абитуриент?", reply_markup=reply_markup
    )

    return CHOOSING_ROLE  # Переход к следующему этапу диалога


async def choose_role(update: Update, context: CallbackContext):
    """Обрабатывает выбор пользователя и отправляет ему соответствующее меню."""
    user_id = update.message.from_user.id
    role = update.message.text.lower().strip()

    logger.info(f"Пользователь {user_id} выбрал: {role}")

    if role not in ["студент", "абитуриент"]:
        await update.message.reply_text("Пожалуйста, выберите 'Студент' или 'Абитуриент'.")
        return CHOOSING_ROLE  # Остаемся в этом состоянии

    add_user(user_id, role)

    if role == "студент":
        keyboard = [
            ["🕔 Расписание отделов"],
            ["🔬 Наука", "🎓 Дипломы и диссертации"],
            ["💵 Стипендии и гранты", "🏆 Чемпионаты и стажировки"],
            ["❓ Задать вопрос"]
        ]
        welcome_text = "Вы выбрали 'Студент'. Вот ваше меню:"
    else:
        keyboard = [
            ["📚 Направления обучения","📝 Общежития"],
            ["📅 Вступительные экзамены", "☎️ Контакты для связи"],
            ["🧑‍💻 Узнай свою ИТ-специализацию"]
        ]
        welcome_text = "Вы выбрали 'Абитуриент'. Вот ваше меню:"

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    logger.info(f"Пользователь {user_id} получил меню {role}")

    return ConversationHandler.END  # Завершаем диалог


def get_start_handlers():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_role)]
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,  # Разрешаем заново входить в диалог
    )

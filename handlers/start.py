from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters
import json
from handlers.rasp import ask_rasp_question
USERS_FILE = "users.json"

# Функция для загрузки пользователей
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функция для сохранения пользователей
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
        # Функция для сохранения пользователей
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Функция для добавления пользователя
def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

async def start(update, context):
    user_id = update.message.from_user.id
    add_user(user_id)
    
    keyboard = [
        ["🕔 Расписание отделов"],
        ["🔬 Наука", "🎓 Дипломы и диссертации"],
        ["💵 Стипендии и гранты", "🏆 Чемпионаты и стажировки"],
        ["❓ Задать вопрос"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text("Выбери из меню  :", reply_markup=reply_markup)

def get_start_handlers():
    return [
        CommandHandler("start", start),
        MessageHandler(filters.Regex(r"^⬅️ Главное меню$"), start)

    ]

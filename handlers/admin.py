import json
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import CallbackContext

USERS_FILE = "users.json"
ADMINS = [242648429]  # 🔴 Укажи реальные Telegram ID администраторов

# Функция для загрузки списка пользователей
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функция рассылки уведомлений
async def notify(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text("❌ У вас нет прав на рассылку!")
        return

    if not context.args:
        await update.message.reply_text("⚠ Использование: /notify <текст сообщения>")
        return

    message_text = " ".join(context.args)
    users = load_users()
    sent_count = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message_text)
            sent_count += 1
        except Exception as e:
            print(f"Ошибка отправки {user_id}: {e}")

    await update.message.reply_text(f"✅ Уведомление отправлено {sent_count} пользователям.")

# Возвращает обработчик для команды /notify
def get_admin_handlers():
    return [CommandHandler("notify", notify)]

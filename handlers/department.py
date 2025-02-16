from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler, filters, ConversationHandler
import logging
from handlers.start import start
from handlers.rasp import ask_rasp_question, rasp_buttons, send_rasp_schedule
from handlers.science import ask_science_question, science_buttons, send_sci_schedule
from handlers.diploma import  ask_diploma_question, dip_buttons, send_dip_schedule
from handlers.stipendia import ask_stip_question, stip_buttons, send_stip_schedule
from handlers.champion import  ask_champ_question, champ_buttons, send_champ_schedule
logger = logging.getLogger(__name__)

ADMINS = {
    "🖥️ Кафедра 41": 242648429,
    "🌐 Кафедра 42": 242648429,
    "👨‍💻 Кафедра 43": 242648429,
    "📊 Кафедра 44": 242648429,
    "⭐️ Деканат ⭐️": 242648429,
}

SELECT_DEPARTMENT, ASK_QUESTION = range(2)


async def ask_department_question(update, context):
    context.user_data.clear()

    # Исключаем "Деканат" из списка кафедр
    departments = [d for d in ADMINS.keys() if d != "⭐️ Деканат ⭐️"]

    keyboard = [["⭐️ Деканат ⭐️"]]  # Добавляем "Деканат" первой строкой
    keyboard += [departments[i:i + 2] for i in range(0, len(departments), 2)]  # Группировка кафедр по 2 в строке
    keyboard.append(["⬅️ Главное меню"])  # Добавляем кнопку в конце

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text("Выберите куда хотите направить вопрос?", reply_markup=reply_markup)

    return SELECT_DEPARTMENT
async def select_department(update, context):
    text = update.message.text
    if text == "⬅️ Главное меню":
        #await update.message.reply_text("Возврат в главное меню.")
        context.user_data.clear()
        await start(update, context)  # Явный вызов функции start
        return ConversationHandler.END

    if text not in ADMINS:
        # Если пользователь нажал "🕔 Расписание отделов"
        if text == "🕔 Расписание отделов":
            await ask_department_question(update, context)  # Перенаправляем на функцию из rasp.py
            return ConversationHandler.END  # Завершаем текущий ConversationHandler
        await update.message.reply_text("Не понимаю,куда хотите отправить вопрос.😢 Попробуйте еще раз.")
        return SELECT_DEPARTMENT

    context.user_data["department"] = text
    keyboard = [["⬅️ Главное меню"]]  # Сокращённый текст кнопки
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=False,
        resize_keyboard=True  # Уменьшаем размер клавиатуры
    )
    await update.message.reply_text(f"Вы выбрали {text}. Напишите вопрос:", reply_markup=reply_markup)
    return ASK_QUESTION

async def handle_question(update, context):
    text = update.message.text
    if text == "⬅️ Главное меню":
        #await update.message.reply_text("Возврат в главное меню.")
        context.user_data.clear()
        await start(update, context)
        return ConversationHandler.END

    department = context.user_data.get("department")
    admin_id = ADMINS.get(department)
    if not admin_id:
        await update.message.reply_text("Ошибка: Не понимаю,куда хотите отправить вопрос😢")
        return ConversationHandler.END

    user = update.message.from_user
    context.user_data["user_id"] = user.id  # Сохраняем user_id
    context.user_data["username"] = user.username  # Сохраняем username

    # Отправляем вопрос администратору
    await context.bot.send_message(
        chat_id=admin_id,
        text=f"Вопрос от @{user.username} ({user.id}) для {department}:\n\n{text}"
    )
    await update.message.reply_text("✅ Вопрос отправлен!")
    context.user_data.clear()
    await start(update, context)
    return ConversationHandler.END

# Возвращает ConversationHandler для раздела
def get_department_handlers():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^❓ Задать вопрос$"), ask_department_question)],
        states={
            SELECT_DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_department)],
            ASK_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Главное меню$"), lambda update, context: ConversationHandler.END)],
    allow_reentry = True  # Разрешает перезапуск диалога
    )

# Главный обработчик ответа администратора
async def handle_admin_reply(update, context):
    text = update.message.text  # Текст сообщения

    # Если текст "Главное меню", перенаправляем в главное меню
    if text == "⬅️ Главное меню":
        await start(update, context)  # Вызов функции start для перехода в главное меню
        return


    # Если администратор нажал "🕔 Расписание отделов"
    if text == "🕔 Расписание отделов":
        await ask_rasp_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return
    if text == "🔬 Наука":
        await ask_science_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return

    if text == "🎓 Дипломы и диссертации":
        await ask_diploma_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return

    if text == "💵 Стипендии и гранты":
        await ask_stip_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return
    if text == "🏆 Чемпионаты и стажировки":
        await ask_champ_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return
    if text in champ_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_champ_schedule(update, context)

    if text in stip_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_stip_schedule(update, context)

    if text in rasp_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_rasp_schedule(update, context)
    # Если это выбор одного из отделов, направляем на функцию для расписания
    if text in dip_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_dip_schedule(update, context)
        return
    if text in science_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_sci_schedule(update, context)
        return


    # Если это ответ на сообщение
    if update.message.reply_to_message:  # Проверяем, является ли сообщение ответом
        original_message = update.message.reply_to_message.text
        if "Вопрос от" in original_message:  # Проверяем, что это ответ на вопрос
            # Извлекаем информацию о пользователе из оригинального сообщения
            user_info = original_message.split("\n\n")[0]
            user_id = int(user_info.split("(")[1].split(")")[0])  # Извлекаем user_id

            # Отправляем ответ пользователю
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"Ответ от администратора:\n\n{update.message.text}"
                )
                await update.message.reply_text("✅ Ответ отправлен пользователю.")
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения пользователю: {e}")
                await update.message.reply_text("❌ Не удалось отправить ответ пользователю.")


# Возвращает обработчик для ответов администратора
def get_admin_reply_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_reply)



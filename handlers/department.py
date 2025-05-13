from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler, filters, ConversationHandler
import logging
from handlers.start import start
from handlers.rasp import ask_rasp_question, rasp_buttons, send_rasp_schedule
from handlers.science import ask_science_question, science_buttons, send_sci_schedule
from handlers.diploma import  ask_diploma_question, dip_buttons, send_dip_schedule
from handlers.stipendia import ask_stip_question, stip_buttons, send_stip_schedule
from handlers.champion import  ask_champ_question, champ_buttons, send_champ_schedule
from handlers.napr import  ask_napr_question, napr_buttons, send_napr_schedule
from handlers.abi import ask_abi_question, abi_buttons, send_abi_schedule
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
    departments = [d for d in ADMINS.keys()]
    keyboard = [departments[i:i + 2] for i in range(0, len(departments), 2)]
    keyboard.append(["⬅️ Главное меню"])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text("Выберите интересующую кафедру:", reply_markup=reply_markup)
    return SELECT_DEPARTMENT
DEPARTMENT_INFO = {
    "🖥️ Кафедра 41": "Кафедра 41\n📞 Телефон: (812) 494-70-41\n📧 Email:  dept41@guap.ru\n👤 Зав. кафедрой: Коржавин Георгий Анатольевич",
    "🌐 Кафедра 42": "Кафедра 42\n📞 Телефон: (812) 494-70-53\n📧 Email: kaf42@guap.ru\n👤 Зав. кафедрой: Мичурин Сергей Владимирович",
    "👨‍💻 Кафедра 43": "Кафедра 43\n📞 Телефон: (812) 494-70-43\n📧 Email:  k43@guap.ru\n👤 Зав. кафедрой: Охтилев Михаил Юрьевич",
    "📊 Кафедра 44": "Кафедра 44\n📞 Телефон: (812) 494-70-44\n📧 Email: kaf44@guap.ru\n👤 Зав. кафедрой: Сергеев Михаил Борисович",
    "⭐️ Деканат ⭐️": "⭐️ Деканат ⭐️\n📞 Телефон: (812) 494-70-40; (812) 312-24-14\n📧 Email: dek4@guap.ru\n👤 Директор Института: Татарникова Татьяна Михайловна\n"
                     "📞 Телефон деканата младших курсов: (812) 708-39-43\n📧 Email деканата младших курсов: dek4gast@guap.ru"
}

async def select_department(update, context):
    text = update.message.text


    if text == "⬅️ Главное меню":
        context.user_data.clear()
        await show_main_menu(update, context)
        return ConversationHandler.END

    if text not in ADMINS:
        await update.message.reply_text("Не понимаю, куда хотите отправить вопрос. 😢 Попробуйте еще раз.")
        return SELECT_DEPARTMENT

    # Показываем информацию о выбранной кафедре
    info = DEPARTMENT_INFO.get(text, "Информация о кафедре не найдена.")
    keyboard = [["⬅️ Главное меню"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(info, reply_markup=reply_markup)

    return SELECT_DEPARTMENT

async def show_main_menu(update, context):
    """Отображаем главное меню без выбора роли."""
    keyboard = [
        ["🕔 Расписание отделов"],
        ["🔬 Наука", "🎓 Дипломы и диссертации"],
        ["💵 Стипендии и гранты", "🏆 Чемпионаты и стажировки"],
        ["❓ Задать вопрос"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text("Главное меню", reply_markup=reply_markup)

async def show_ABI_menu(update, context):
        """Отображаем главное меню без выбора роли."""
        keyboard = [
            ["📚 Направления обучения", "📝 Общежития"],
            ["📅 Вступительные экзамены", "☎️ Контакты для связи"],
            ["🧑‍💻 Узнай свою ИТ-специализацию"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text("Главное меню", reply_markup=reply_markup)

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
        await show_main_menu(update, context)  # Вызов функции start для перехода в главное меню
        return

    if text == "⬅️ Меню":
        await show_ABI_menu(update, context)  # Вызов функции start для перехода в главное меню
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
    if text == "📚 Направления обучения":
        await ask_napr_question(update, context)  # Перенаправляем на функцию для запроса отдела
        return
    if text in champ_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_champ_schedule(update, context)

    if text in stip_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_stip_schedule(update, context)
    if text in abi_buttons:
        # В зависимости от выбранного отдела, отправляем расписание
        await send_abi_schedule(update, context)
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
    if text in napr_buttons:
        await send_napr_schedule(update, context)
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


def get_department_handlers():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^❓ Задать вопрос$"), ask_department_question)],
        states={
            SELECT_DEPARTMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_department)
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^⬅️ Главное меню$"), lambda update, context: show_main_menu(update, context)),
        ],
        allow_reentry=True
    )

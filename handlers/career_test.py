from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

QUESTION, = range(1)

questions = [
    ("Какую деятельность вы считаете наиболее интересной?",
     ["Проектировать сети", "Автоматизировать бизнес", "Создавать графику", "Монтировать видео", "Обрабатывать данные",
      "Программировать приложения"]),

    ("Какой проект вам хотелось бы реализовать?",
     ["Умный дом", "CRM-система", "Мобильный интерфейс", "Видео-презентация", "Обработка данных", "Веб-сервис"]),

    ("Какие школьные предметы вам ближе?",
     ["Информатика и физика", "Математика и экономика", "Изо и черчение", "Литература и обществознание",
      "Алгебра и логика", "Информатика и математика"]),

    ("Где бы вы хотели работать?",
     ["Инженером по сетям", "Бизнес-аналитиком", "UX/UI-дизайнером", "Специалистом по медиа", "IT-специалистом",
      "Разработчиком"]),

    ("Что вас больше вдохновляет?",
     ["Железо и техника", "Оптимизация процессов", "Визуальное оформление", "Контент и аудитория",
      "Информация и структура", "Алгоритмы"]),

    ("Что вы выберете в учебном проекте?",
     ["Железо и сети", "Базы данных", "UI-прототип", "Рекламный ролик", "Таблицы и отчёты", "Функциональный сервис"]),

    ("Какой формат обучения вам ближе?",
     ["Лаборатории и техника", "Бизнес-кейсы", "Графика и UI", "Проекты в медиа", "Документы и данные",
      "Программирование"]),

    ("Что вам по душе?",
     ["Устройства и сети", "IT и экономика", "Визуал и стиль", "Видео и звук", "Инфосистемы", "Архитектура ПО"]),

    ("Какие ваши сильные стороны?",
     ["Техника и инженерия", "Анализ в бизнесе", "Креатив и визуал", "Коммуникации", "Точность и структура",
      "Программирование"]),

    ("Кем вы видите себя через 5 лет?",
     ["Сисадмином", "Аналитиком", "IT-дизайнером", "Медиа-специалистом", "IT-менеджером", "Разработчиком"])
]

direction_codes = [
    "09.03.01 — Информатика и вычислительная техника (Компьютерные технологии, системы и сети)",
    "09.03.02 — Информационные системы и технологии (в бизнесе)",
    "09.03.02 — Информационные системы и технологии (в дизайне)",
    "09.03.02 — Информационные системы и технологии (в медиаиндустрии)",
    "09.03.03 — Прикладная информатика (в информационной сфере)",
    "09.03.04 — Программная инженерия (Проектирование программных систем)"
]


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q_index"] = 0
    context.user_data["scores"] = [0] * 6
    return await ask_question(update, context)


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_index = context.user_data["q_index"]
    if q_index >= len(questions):
        return await show_result(update, context)

    question, options = questions[q_index]

    # Формируем клавиатуру по два варианта в строке
    keyboard = [options[i:i + 2] for i in range(0, len(options), 2)]
    keyboard.append(["⬅️ Меню"])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(f"Вопрос {q_index + 1} из {len(questions)}:\n\n{question}",
                                    reply_markup=reply_markup)
    return QUESTION


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text

    if answer == "⬅️ Меню":
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=main_menu())
        return ConversationHandler.END

    q_index = context.user_data["q_index"]
    _, options = questions[q_index]

    try:
        selected = options.index(answer)
    except ValueError:
        await update.message.reply_text("Пожалуйста, выберите вариант из предложенных.")
        return QUESTION

    context.user_data["scores"][selected] += 1
    context.user_data["q_index"] += 1
    return await ask_question(update, context)


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scores = context.user_data["scores"]
    best_index = scores.index(max(scores))
    direction = direction_codes[best_index]

    reply_markup = ReplyKeyboardMarkup([["⬅️ Меню"]], resize_keyboard=True)

    await update.message.reply_text(
        f"🎓 По результатам теста, вам подойдёт направление:\n\n👉 *{direction}*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


# Главное меню (восстановление клавиатуры)
def main_menu():
    return ReplyKeyboardMarkup([
        ["📚 Направления обучения", "📝 Общежития"],
        ["📅 Вступительные экзамены", "☎️ Контакты для связи"],
        ["🧑‍💻 Узнай свою ИТ-специализацию"]
    ], resize_keyboard=True)


def get_career_test_handler():
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(r"🧑‍💻 Узнай свою ИТ-специализацию"), start_test)
        ],
        states={
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)]
        },
        fallbacks=[],
    )

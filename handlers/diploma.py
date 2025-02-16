from telegram import ReplyKeyboardMarkup
# Основной обработчик для меню с подразделениями
async def ask_diploma_question(update, context):
    context.user_data.clear()  # Очистим данные пользователя
    keyboard = [
        ["🖥️ Кафедра 41", "🌐 Кафедра 42"],
        ["‍💻 Кафедра 43", "📊 Кафедра 44"],
        ["⬅️ Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text("На какой кафедре ты обучаешься?", reply_markup=reply_markup)


dip_buttons = [
        "🖥️ Кафедра 41", "🌐 Кафедра 42",
        "‍💻 Кафедра 43", "📊 Кафедра 44",
        "⬅️ Главное меню"
    ]

# Функция отправки расписания по выбранному отделу
async def send_dip_schedule(update, context):
    department = update.message.text  # Извлекаем текст выбранного отдела

    # Пример отправки расписания для каждого отдела (вам нужно будет заменить эти строки на актуальное расписание)
    if department == "🖥️ Кафедра 41":
        schedule = ("<b>Правила и последовательность сдачи диплома или диссертации</b>\n\n"
                    "1️⃣ <b>Согласование с руководителем</b>\n"
                    "Написать дипломную работу и утвердить её с научным руководителем.\n\n"
                    "2️⃣ <b>Проверка на антиплагиат</b>\n"
                    "Отправить диплом на проверку антиплагиата ВУЗа на почту:\n"
                    "📩 raskopina.anastasia@yandex.ru (Преподаватель: Раскопина Анастасия Сергеевна).\n"
                    "Дождаться справки о проверке (если не пройдено — доработать и отправить снова).\n\n"
                    "3️⃣ <b>Получение отзыва научного руководителя</b>\n"
                    "После передать диплом с справкой на антиплагиат руководителю для написания отзыва.\n"
                    "В отзыве должны быть указаны проценты оригинальности работы.\n\n"
                    "4️⃣ <b>Рецензирование (только для магистров)</b>\n"
                    "С дипломом и отзывом обратиться к рецензенту, назначенному по приказу.\n"
                    "Получить рецензию на работу.\n"
                    "Рецензенту нужно скинуть работу минимум за неделю до сдачи!!!\n\n"
                    "5️⃣ <b>Отправка работы на экспертизу</b>\n"
                    "Отправить текст ВКР для экспертизы Виктору Ивановичу:\n"
                    "📩 ivi@guap.ru\n"
                    "Это можно сделать сразу после готовности работы, без ожидания других этапов.\n\n"
                    "6️⃣ <b>Передача диплома на кафедру</b>\n"
                    "Подписанную и прошитую дипломную работу, вместе с отзывом и рецензией, "
                    "передать на кафедру Загураевой Марии Викторовне.\n\n"
                    "❗️ <b>Важно</b>\n"
                    "✔️ Проверку антиплагиата лучше проводить за 15 дней до защиты.\n"
                    "✔️ У вас всего 2 попытки пройти Антиплагиат.\n"
                    "✔️ Для бакалавров процент оригинальности должен быть минимум 70%.\n"
                    "✔️ Для магистров процент оригинальности должен быть минимум 80%.\n\n"
         
                    '<b>❣️Также интересные примеры работ студентов можно найти на нашей <a href="https://guap.ru/vitrina4">Витрине Проектов</a></b>\n'

                    )
    elif department == "🌐 Кафедра 42":
        schedule = ("Нужна инфомармация. Пример 41 кафедра")
    elif department == "‍💻 Кафедра 43":
        schedule = ("Нужна инфомармация. Пример 41 кафедра")
    elif department == "📊 Кафедра 44":
        schedule = ("Нужна инфомармация. Пример 41 кафедра")

    else:
        schedule = "Не удалось найти кафедру."

    await update.message.reply_text(schedule, parse_mode="HTML")
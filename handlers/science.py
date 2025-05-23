from telegram import ReplyKeyboardMarkup

from telegram.ext import CommandHandler, MessageHandler, filters
import logging
# Основной обработчик для меню с подразделениями
async def ask_science_question(update, context):
    context.user_data.clear()  # Очистим данные пользователя
    keyboard = [
        ["Прикладной искусственный интеллект: перспективы и риски"],
        ["Обработка, передача и защита информации в компьютерных системах"],
        ["Международная  студенческая научная конференция ГУАП"],
        ["Профессорский состав", "Наши сообщества"],
        ["⬅️ Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text("Какая информация тебя интересует?", reply_markup=reply_markup)


science_buttons = [
"Прикладной искусственный интеллект: перспективы и риски",
        "Обработка, передача и защита информации в компьютерных системах",
        "Международная  студенческая научная конференция ГУАП",
        "Профессорский состав", "Наши сообщества",
    ]

async def send_sci_schedule(update, context):
    department = update.message.text  # Извлекаем текст выбранного отдела

    # Пример отправки расписания для каждого отдела (вам нужно будет заменить эти строки на актуальное расписание)
    if department == "Прикладной искусственный интеллект: перспективы и риски":
        schedule = (
            "<b>Международная конференция «Прикладной искусственный интеллект: перспективы и риски»</b>\n\n"
            "<b>Цель международной конференции —</b> обмен опытом и идеями в области создания высокотехнологичных продуктов "
            "и сервисов с применением технологий искусственного интеллекта, освещение проблем, "
            "связанных с угрозами от влияния искусственного интеллекта, а также перспектив развития технологий "
            "искусственного интеллекта в профильных для ГУАП сферах\n\n"
            
            "<b>Задачи конференции:</b>\n"
            "🔹Определение перспективных технологий искусственного интеллекта для ядерных направлений развития "
            "ГУАП программы стратегического академического лидерства «Приоритет 2030».\n"
            "🔹Развитие сотрудничества научных школ ГУАП с производственными предприятиями, использующими технологии "
            "искусственного интеллекта в своей деятельности.\n"
            "🔹Применение технологий искусственного интеллекта в образовательном процессе проблем и рисков, возникающих "
            "при внедрении технологий искусственного интеллекта в прикладных областях.\n\n"
            
            "<b>Основные научные направления международной конференции:</b>\n"
            "▪️Технологии искусственного интеллекта в аэрокосмическом приборостроении и инженерии\n"
            "▪️Технологии искусственного интеллекта в образовании\n"
            "▪️Разработка интеллектуальных интерфейсов\n"
            "▪️Прикладные интеллектуальные и информационные системы\n"
            "▪️Искусственный интеллект в информационной безопасности\n\n"


            "По организационным вопросам и вопросам оформления докладов обращаться на электронную почту: sns4@guap.ru\n\n"
            '<b>Подробнее на официальном <a href="https://guap.ru/n/aai">сайте</a></b>\n'
        "\n")

    elif department == "Обработка, передача и защита информации в компьютерных системах":
        schedule = ("<b>Международная конференция «Обработка, передача и защита информации в компьютерных системах»</b>\n\n"
        "<b>Цель международной конференции —</b> создание пространства для обмена информацией и результатами "
        "исследовательской работы научно-педагогических работников, молодых ученых, аспирантов, соискателей и "
        "студентов в области передачи, обработки и защиты информации в компьютерных системах.\n\n"
           
        "<b>Задачи конференции:</b>"
        "🔹Аккумулировать научные достижения и ознакомить профессорско-преподавательский состав, аспирантов и студентов"
        " учебных заведений, специалистов предприятий с результатами научных разработок и выполненных прикладных "
        "исследований в области передачи, обработки и защиты информации в компьютерных системах.\n"
        "🔹Раскрыть и совершенствовать профессиональные навыки студентов, магистров и аспирантов, презентовать их интеллектуальный потенциал.\n"
        "🔹Мотивировать молодых специалистов к активному участию в деятельности предприятий и организаций, заинтересовать в "
        "высоких показателях результативности. мотивировать молодых специалистов к активному участию в "
        "деятельности предприятий и организаций, заинтересовать в высоких показателях результативности.\n\n"
                    
        "<b>Основные научные направления международной конференции:</b>\n"
        "▪️Разработка вычислительных систем на основе современной элементной базы.\n"
         "▪️Методы и алгоритмы цифровой обработки сигналов и изображений.\n"
        "▪️Системный анализ и проектирование систем автоматического управления.\n"
        "▪️Машинное обучение и искусственный интеллект.\n"
        "▪️Виртуальная и дополненная реальность.\n"
        "▪️Математическое моделирование.\n"
        "▪️Разработка программного обеспечения.\n\n"

         "По организационным вопросам и вопросам оформления докладов обращаться на электронную почту: sns4@guap.ru\n\n"
        '<b>Подробнее на официальном <a href="https://guap.ru/m/ptpi">сайте</a></b>'
                    "\n")

    elif department == "Международная  студенческая научная конференция ГУАП":
        schedule = ("<b>Международная  студенческая научная конференция ГУАП</b>\n\n"
                    "На протяжении многих лет проведение студенческих научных конференций и выставок научно- технического "
                    "творчества студентов ГУАП являются важнейшими итоговыми научными студенческими мероприятиями, в которых "
                    "принимают участие все факультеты и кафедры ГУАП, а также студенты из российских и иностранных университетов.\n\n"
                    "География участников и их количество растет с каждым годом. В 2024 году в конференции приняли участие 1147 студентов."
                    " По результатам работы 69 научных секций свыше 300 лучших, из представленных студентами 1069 докладов рекомендованы к "
                    "опубликованию в сборнике материалов конференции.\n\n"
                    "Научные работы студентов посвящены актуальным проблемам авиационного и аэрокосмического приборостроения, проблемам развития "
                    "информационных технологий, киберфизических систем, робототехники, радиотехники, электроники и связи, современным проблемам "
                    "экономики, управления, философии и права.\n\n"
                    "<b>Направления работы</b>\n"
                    "️▪️Прикладная математика, физика и механика\n"
                    "▪️Аэрокосмические приборы и системы\n"
                    "▪️Радиотехника, электроника и связь\n"
                    "▪️Системы управления, робототехника, электроэнергетика\n"
                    "▪️Киберфизические системы\n"
                    "▪️Вычислительные системы и программирование\n"
                    "▪️Информационные системы и защита информации\n"
                    "▪️Приборостроение в медицине и биологии\n"
                    "▪️Метрология, стандартизация и сертификация\n"
                    "▪️Гуманитарные науки\n"
                    "▪️Военные науки\n"
                    "▪️Экономика и менеджмент\n"
                    "▪️Юридические \n\n"
                    '<b>Подробнее на официальном <a href="https://guap.ru/msnk">сайте</a></b>'
                    "\n")

    elif department == "Профессорский состав":
        schedule = ("В Институте информационных технологий и программирования работает <b>12 профессоров</b>:\n\n"
                    "1. Коржавин Георгий Анатольевич\n"
                    "2. Татарникова Татьяна Михайловна\n"
                    "3. Шепета Александр Павлович\n"
                    "4. Рождественский Юрий Владимирович\n"
                    "5. Мичурин Сергей Владимирович\n"
                    "6. Фомин Владимир Владимирович\n"
                    "7. Охтилев Михаил Юрьевич\n"
                    "8. Колесникова Светлана Ивановна\n"
                    "9. Скобцов Юрий Александрович\n"
                    "10. Балонин Николай Алексеевич\n"
                    "11. Гордеев Александр Владимирович \n"
                    "12. Сергеев Михаил Борисович \n\n"
                    '<b>Подробнее о тематиках научных исследований на <a href="https://new.guap.ru/i04/science">сайте</a></b>'"\n")

    elif department == "Наши сообщества":
        schedule = (
        "✔️Ищешь информацию об актуальных научно-исследовательских конкурсах, конференциях, профессиональных олимпиадах и грантах?\n"
        "✔️Хочешь узнать правила оформления заявки на государственную регистрацию изобретения или программы?\n"
        "✔️Желаешь обменяться опытом научно-исследовательской деятельности с товарищами иполучить ответы на интересующие "
        "Вас вопросы, касающиеся УНИДС?\n\n"
        '<b> Тогда присоединяйся к нашему сообществу в <a href="https://vk.com/suaidept41science">Вконтакте.</a></b>'
        "\n")
    else:
        schedule = "Не удалось найти."

    await update.message.reply_text(schedule, parse_mode="HTML")

import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Ваш ID чата, куда будут отправляться проблемы (можно узнать через бота @userinfobot в Telegram)
ADMIN_CHAT_ID = 'YOUR_ADMIN_CHAT_ID'

# Функция для создания главной клавиатуры
def start(update: Update, context: CallbackContext) -> None:
    schedule_button = KeyboardButton("Розклад")
    bells_button = KeyboardButton("Дзвоники")
    problem_button = KeyboardButton("Повідомити про проблему")
    keyboard = ReplyKeyboardMarkup([[schedule_button], [bells_button], [problem_button]], resize_keyboard=True)
    update.message.reply_text('Привіт! Що вас цікавить?', reply_markup=keyboard)


# Функция для обработки нажатия кнопки "Розклад"
def class_schedule(update: Update, context: CallbackContext) -> None:
    class_buttons = [KeyboardButton(f"Розклад {i} класу") for i in range(1, 10)]
    senior_classes_buttons = [KeyboardButton("Розклад 10 класу"), KeyboardButton("Розклад 11 класу")]
    main_menu_button = KeyboardButton("На головний екран")

    keyboard = ReplyKeyboardMarkup(
        [class_buttons[i:i + 2] for i in range(0, len(class_buttons), 2)] + [senior_classes_buttons,
                                                                             [main_menu_button]],
        resize_keyboard=True
    )
    update.message.reply_text('Виберіть клас:', reply_markup=keyboard)


# Функция для обработки выбора подклассов
def sub_class_schedule(update: Update, context: CallbackContext) -> None:
    selected_class = update.message.text.split()[1]
    if selected_class in ['6', '7']:
        sub_class_buttons = [KeyboardButton(f"{selected_class}-{letter}") for letter in ['А', 'Б', 'В', 'Г']]
    else:
        sub_class_buttons = [KeyboardButton(f"{selected_class}-{letter}") for letter in ['А', 'Б', 'В']]
    back_button = KeyboardButton("Назад до вибору класу")

    keyboard = ReplyKeyboardMarkup([sub_class_buttons] + [[back_button]], resize_keyboard=True)
    update.message.reply_text(f'Виберіть підклас для {selected_class} класу:', reply_markup=keyboard)


# Функция для обработки выбора подкласса (например, 1-А)
def sub_class_schedule_selected(update: Update, context: CallbackContext) -> None:
    selected_sub_class = update.message.text
    file_path = f"rozklad/{selected_sub_class}_class.txt"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            schedule = file.read()
        update.message.reply_text(f'Розклад для {selected_sub_class}:\n\n{schedule}')
    else:
        update.message.reply_text(f'Вибачте, розклад для {selected_sub_class} відсутній.')


# Функция для обработки 10 и 11 классов
def senior_class_schedule(update: Update, context: CallbackContext) -> None:
    selected_class = update.message.text
    class_number = selected_class.split()[1]
    file_path = f"rozklad/{class_number}_class.txt"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            schedule = file.read()
        update.message.reply_text(f'Розклад для {class_number} класу:\n\n{schedule}')
    else:
        update.message.reply_text(f'Вибачте, розклад для {class_number} класу відсутній.')


# Функция для обработки нажатия кнопки "Дзвоники"
def bells_schedule(update: Update, context: CallbackContext) -> None:
    file_path = 'dzvonki/vsa_sc.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            bells = file.read()
        update.message.reply_text(f'Дзвоники:\n\n{bells}')
    else:
        update.message.reply_text('Вибачте, інформація про дзвоники відсутня.')


# Функция для отправки проблемы в указанный чат
def handle_problem(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id

    message = f"Нова проблема від {user_name} (ID: {user_id}):\n\n{user_message}"
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    update.message.reply_text('Дякуємо! Ваша проблема була надіслана адміністратору.')


# Функция для возврата на главный экран
def return_to_main_menu(update: Update, context: CallbackContext) -> None:
    start(update, context)


# Функция для возврата к выбору класса
def back_to_class_selection(update: Update, context: CallbackContext) -> None:
    class_schedule(update, context)


def main():
    TOKEN = '7653540833:AAEf6OUt6p2b5OioBjrA1FJy3EaHNlzJj80'
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(
        Filters.regex('Розклад 1|Розклад 2|Розклад 3|Розклад 4|Розклад 5|Розклад 6|Розклад 7|Розклад 8|Розклад 9'),
        sub_class_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('Розклад 10 класу|Розклад 11 класу'), senior_class_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('Розклад'), class_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('Дзвоники'), bells_schedule))
    dispatcher.add_handler(MessageHandler(Filters.regex('На головний екран'), return_to_main_menu))
    dispatcher.add_handler(MessageHandler(Filters.regex('Назад до вибору класу'), back_to_class_selection))

    # Обработчик для выбора подклассов
    dispatcher.add_handler(
        MessageHandler(Filters.regex('1-А|1-Б|1-В|2-А|2-Б|2-В|3-А|3-Б|3-В|5-А|5-Б|5-В|'
                                     '6-А|6-Б|6-В|6-Г|7-А|7-Б|7-В|7-Г|8-А|8-Б|8-В|'
                                     '9-А|9-Б|9-В|10|11|'), sub_class_schedule_selected))

    # Обработчик для описания проблемы
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_problem))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

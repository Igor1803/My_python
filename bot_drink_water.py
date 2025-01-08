import telebot
import datetime
import time
import threading
import random

# Замените 'YOUR_TOKEN' на токен вашего бота
bot = telebot.TeleBot('7918830452:AAF8oKPCoSWEp36n7SPE0HMp2HdlW1Nnfsk')

# Список фактов о воде
facts = [
    "Вода на Земле может быть старше самой Солнечной системы.",
    "Горячая вода замерзает быстрее холодной (эффект Мпемба).",
    "Больше воды в атмосфере, чем во всех реках мира."
]

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я чат-бот, который будет напоминать тебе пить водичку!')

# Команда /fact
@bot.message_handler(commands=['fact'])
def fact_message(message):
    random_fact = random.choice(facts)
    bot.reply_to(message, f'Лови факт о воде: {random_fact}')

# Функция для отправки напоминаний
def send_reminders(chat_id):
    first_rem = "09:00"
    second_rem = "13:10"
    end_rem = "18:00"

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == first_rem or now == second_rem or now == end_rem:
            bot.send_message(chat_id, "Напоминание - выпей стакан воды!")
            time.sleep(61)  # Задержка, чтобы избежать повторной отправки
        time.sleep(1)

# Запуск потока для напоминаний
@bot.message_handler(commands=['start'])
def start_reminders(message):
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

# Запуск бота
bot.polling(none_stop=True)
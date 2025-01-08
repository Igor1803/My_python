import telebot
import time
import threading

# Укажите ваш токен бота
BOT_TOKEN = '7509898676:AAHQx-9g14m-ztU-qSeI0AWhJqonbkabUDI'

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения ID чатов пользователей, которые подписались на напоминания
subscribed_users = set()

# Функция для отправки напоминания
def send_water_reminder():
    while True:
        time.sleep(6 * 60 * 60)  # 6 часов в секундах
        for chat_id in subscribed_users:
            bot.send_message(chat_id, "Пора пить воду! 💧")

# Запускаем поток для отправки напоминаний
reminder_thread = threading.Thread(target=send_water_reminder)
reminder_thread.daemon = True
reminder_thread.start()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который напоминает пить воду. Используй команду /subscribe, чтобы подписаться на напоминания.")

# Обработчик команды /subscribe
@bot.message_handler(commands=['subscribe'])
def handle_subscribe(message):
    subscribed_users.add(message.chat.id)
    bot.send_message(message.chat.id, "Вы подписались на напоминания о воде. Каждые 6 часов я буду вас напоминать! 💧")

# Обработчик команды /unsubscribe
@bot.message_handler(commands=['unsubscribe'])
def handle_unsubscribe(message):
    if message.chat.id in subscribed_users:
        subscribed_users.remove(message.chat.id)
        bot.send_message(message.chat.id, "Вы отписались от напоминаний о воде. Если захотите снова подписаться, используйте команду /subscribe.")
    else:
        bot.send_message(message.chat.id, "Вы не были подписаны на напоминания.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)


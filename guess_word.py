import asyncio
from bs4 import BeautifulSoup
import requests
from googletrans import Translator

# Создаём функцию, которая будет получать информацию
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")

        # Получаем слово
        english_word = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        # Чтобы программа возвращала словарь
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    # Функция, которая сообщит об ошибке, но не остановит программу
    except Exception as e:
        print("Произошла ошибка:", e)

# Функция для перевода текста на русский язык
async def translate_to_russian(text):
    translator = Translator()
    translation = await translator.translate(text, dest='ru')
    return translation.text

# Создаём функцию, которая будет делать саму игру
async def word_game():
    print("Добро пожаловать в игру")
    while True:
        # Создаём функцию, чтобы использовать результат функции-словаря
        word_dict = get_english_words()
        if word_dict:
            word = word_dict.get("english_word")
            word_definition = word_dict.get("word_definition")

            # Переводим слово и определение на русский язык
            translated_word = await translate_to_russian(word)
            translated_definition = await translate_to_russian(word_definition)

            # Начинаем игру
            print(f"Значение слова - {translated_definition} ( {translated_word})")
            user = input("Что это за слово? ")
            if user.lower() == translated_word.lower():
                print("Всё верно!")
            else:
                print(f"Ответ неверный, было загадано это слово - {translated_word}")

            # Создаём возможность закончить игру
            play_again = input("Хотите сыграть ещё раз? д/н ")
            if play_again.lower() != "д":
                print("Спасибо за игру!")
                break

asyncio.run(word_game())
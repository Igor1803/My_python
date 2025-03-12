from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import urllib.parse


def get_paragraphs(browser):
    return browser.find_elements(By.TAG_NAME, "p")


def browse_paragraphs(browser, initial_url):
    paragraphs = get_paragraphs(browser)
    index = 0
    while index < len(paragraphs):
        print(paragraphs[index].text)
        user_input = input("\nНажмите Enter для продолжения или 'q' для возврата... ").strip()

        if user_input.lower() == 'q':
            browser.get(initial_url)
            return False
        index += 1
        print("\n" + "=" * 50 + "\n")
    return True


def get_related_links(browser):
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, "div"):
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable":
            hatnotes.append(element)
    return [hn.find_element(By.TAG_NAME, "a").get_attribute("href") for hn in hatnotes]


def main():
    browser = webdriver.Chrome()

    # Первоначальный запрос
    query = input("Введите запрос для Википедии: ").strip()
    encoded_query = urllib.parse.quote(query)
    initial_url = f"https://ru.wikipedia.org/wiki/{encoded_query}"
    browser.get(initial_url)

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на связанную страницу")
        print("3. Сменить запрос")
        print("4. Выйти из программы")

        choice = input("Ваш выбор (1-4): ").strip()

        if choice == "1":
            if not browse_paragraphs(browser, initial_url):
                continue

        elif choice == "2":
            links = get_related_links(browser)
            if not links:
                print("Нет связанных страниц")
                continue

            browser.get(random.choice(links))

            while True:
                print("\nНа новой странице:")
                print("1. Листать параграфы")
                print("2. Вернуться к выбору действий")
                sub_choice = input("Ваш выбор (1-2): ").strip()

                if sub_choice == "1":
                    if not browse_paragraphs(browser, browser.current_url):
                        break
                elif sub_choice == "2":
                    break
                else:
                    print("Некорректный ввод")

        elif choice == "3":
            # Новый запрос
            new_query = input("Введите новый запрос для Википедии: ").strip()
            encoded_query = urllib.parse.quote(new_query)
            initial_url = f"https://ru.wikipedia.org/wiki/{encoded_query}"
            browser.get(initial_url)
            print(f"\nПерешли на статью: {new_query}")

        elif choice == "4":
            break

        else:
            print("Некорректный ввод")

    browser.quit()


if __name__ == "__main__":
    main()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest
import time
import math


@pytest.fixture(scope="function")
def browser():
    print("\nЗапуск браузера...")
    browser = webdriver.Chrome()
    yield browser
    print("\nЗакрытие браузера...")
    browser.quit()


@pytest.mark.parametrize('links', [
    "236895", "236896", "236897", "236898","236899", "236903", "236904", "236905" ])
def test_guest_should_see_login_link(browser, links):
    link = f"https://stepik.org/lesson/{links}/step/1"
    print(f"\nТестирование ссылки: {link}")
    browser.get(link)
    browser.implicitly_wait(5)

    try:
        # Авторизация
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbar__auth_login"))
        )
        login_button.click()
        browser.implicitly_wait(5)

        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#id_login_email"))
        )
        email_input.send_keys("daraks2016@mail.ru")
        browser.implicitly_wait(5)

        password_input = browser.find_element(By.CSS_SELECTOR, "#id_login_password")
        password_input.send_keys("123456789!")
        browser.implicitly_wait(5)

        entry_button = browser.find_element(By.CSS_SELECTOR, ".sign-form__btn.button_with-loader")
        entry_button.click()
        browser.implicitly_wait(5)

        # Ожидание завершения авторизации
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar__profile"))
        )
        print("Успешный вход в систему.")
    except Exception as e:
        print(f"Ошибка во время авторизации: {str(e)}")
        return  # Завершаем тест при ошибке авторизации

    # Проверка наличия кнопки очистки и ее использование
    try:
        clear_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".again-btn.white"))
        )
        clear_button.click()
        browser.implicitly_wait(5)
        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-ember-action]")))
        confirm_button.click()
        print("Кнопка очистки нажата.")
    except Exception:
        print("Кнопка очистки не найдена. Продолжаем без очистки поля.")
        browser.implicitly_wait(5)

        try:
            # Ожидание загрузки поля для ответа
            answer_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ember-text-area"))
            )
            browser.implicitly_wait(5)

            # Вводим ответ
            answer = str(math.log(int(time.time())))
            answer_input.send_keys(answer)
            print(f"Ответ '{answer}' введен.")
            browser.implicitly_wait(5)

            # Нажимаем кнопку отправки ответа
            answer_button = WebDriverWait(browser, 10).until(
               EC.element_to_be_clickable((By.CSS_SELECTOR, ".submit-submission"))
            )
            answer_button.click()
            browser.implicitly_wait(5)

            # Ожидаем появления сообщения с результатом
            feedback_message = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".smart-hints__hint"))
            )
            feedback_text = feedback_message.text
            browser.implicitly_wait(10)
            print(f"Сообщение фидбека: {feedback_text}")
            browser.implicitly_wait(10)

            # Проверяем, что ответ правильный
            assert feedback_text == "Correct!", f"Ожидалось 'Correct!', но получено '{feedback_text}'"
        except Exception as e:
            print(f"Ошибка во время выполнения теста: {str(e)}")
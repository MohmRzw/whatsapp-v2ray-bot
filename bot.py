import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import qrcode
import os

# فایل پیکربندی
from config import ADMIN_PHONE, AUTO_REPLY

# راه‌اندازی WebDriver
def start_bot():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=./user_data')  # برای ذخیره سشن‌ها
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--headless')  # برای اجرای در پس‌زمینه
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://web.whatsapp.com/")
    print("QR code را اسکن کنید.")

    while True:
        try:
            # منتظر بودن برای بارگذاری واتساپ وب
            driver.find_element(By.XPATH, '//*[@id="pane-side"]')
            break
        except:
            time.sleep(2)

    print("اتصال برقرار شد!")
    return driver

# ارسال پیام به ادمین
def send_message_to_admin(driver, message):
    try:
        driver.find_element(By.XPATH, f'//span[@title="{ADMIN_PHONE}"]').click()
        time.sleep(1)
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
        message_box.send_keys(message + Keys.RETURN)
        print(f"پیام به ادمین فرستاده شد: {message}")
    except Exception as e:
        print("ارسال پیام به ادمین با مشکل مواجه شد:", e)

# دریافت پیام‌های جدید
def check_new_messages(driver):
    while True:
        try:
            unread_chats = driver.find_elements(By.XPATH, '//*[@class="_2K2tI"]')
            if len(unread_chats) > 0:
                for chat in unread_chats:
                    chat.click()
                    time.sleep(1)

                    # گرفتن آخرین پیام
                    last_message = driver.find_element(By.XPATH, '//*[@class="_1Gy50"]')
                    print(f"پیام جدید دریافت شد: {last_message.text}")

                    # ارسال جواب اتوماتیک
                    send_message_to_admin(driver, AUTO_REPLY)
                    # ارسال پیام به ادمین
                    send_message_to_admin(driver, last_message.text)
                    
            time.sleep(5)
        except Exception as e:
            print("خطا در بررسی پیام‌ها:", e)

# اجرای ربات
if __name__ == "__main__":
    driver = start_bot()
    check_new_messages(driver)

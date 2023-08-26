from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
import helpers

load_dotenv()

driver = webdriver.Chrome()

BASE_URL = os.getenv("BASE_URL")
ADMIN_URL = BASE_URL + "/admin"
USERS_URL = BASE_URL + "/users"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print(ADMIN_URL)

try:
    # Go to the login page
    driver.get(ADMIN_URL)

    # inserts username and password & logs in
    username_field = driver.find_element(By.ID, "user_email")
    password_field = driver.find_element(By.ID, "user_password")

    username_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(By.NAME, "commit")
    login_button.click()

    # Go to the users page
    driver.get(USERS_URL)

    user_data = []

    table = driver.find_element(By.ID, "users")
    links = table.find_elements(By.TAG_NAME, "a")


    unique_urls = set()
    for link in links:
        link_url = link.get_attribute("href")
        if link_url.startswith(USERS_URL) and not link_url.endswith("/destroy"):
            unique_urls.add(link_url)

    for link_url in unique_urls:
        driver.get(link_url)
        user_info = {}
        user_info["name"] = driver.find_element(By.NAME, "registration[name]").get_attribute("value")
        user_info["phone"] = driver.find_element(By.NAME, "registration[phone]").get_attribute("value")
        user_info["legal_age"] = "YES" if driver.find_element(By.NAME, "registration[over_eighteen]").is_selected() else "NO"
        user_info["approved"] = "YES" if driver.find_element(By.NAME, "registration[approved]").is_selected() else "NO"
        user_info["paid"] = "YES" if driver.find_element(By.NAME, "registration[paid]").is_selected() else "NO"
        user_data.append(user_info)
    
    helpers.write_csv(user_data, "user_data.csv")
    

finally:
    driver.quit()


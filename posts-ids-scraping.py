
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time

def clean_post_id(post_id):
    if "?" in post_id:
        post_id = post_id.split("?")[0]
    return post_id


def check_and_add_post_id(post_id, post_list):
    cleaned_post_id = clean_post_id(post_id)
    if cleaned_post_id not in post_list:
        post_list.append(cleaned_post_id)


def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com")
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "pass")
    password_field.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR,'button[name="login"]')
    login_button.click()
    time.sleep(5)


def scrape_posts(driver, page_url, post_limit):
    login_to_facebook(driver, "adresse_email@gmail.com", "mot de passe")
    driver.get(page_url)
    post_urls = []

    while len(post_urls) < post_limit:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        post_links = driver.find_elements(By.CSS_SELECTOR, "[href*=\"posts/\"]")
        for post_link in post_links:
            post_url = post_link.get_attribute("href")
            post_id = post_url.split("posts/")[1]
            check_and_add_post_id(post_id, post_urls)

    return post_urls

s = Service(r"C:\\Windows\\System32\\chromedriver.exe")

driver = webdriver.Chrome(service=s)

page_url = "https://www.facebook.com/BanqueZitouna"
post_limit = 1000

post_urls = scrape_posts(driver, page_url, post_limit)

client = MongoClient("mongodb://localhost:27017/")
db = client['mydatabase']
collection = db['postids_Zitouna1']
for post_id in post_urls:
    post_data = {
        'post_id': post_id,
        'scraped_time': datetime.now()
    }
    collection.insert_one(post_data)

driver.quit()



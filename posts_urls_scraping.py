from selenium import webdriver
import time
from datetime import datetime
from pymongo import MongoClient


def clean_post_id(post_url):
    if "?" in post_url:
        post_url = post_url.split("?")[0]
    return post_url


def check_and_add_post_id(post_url, post_list):
    cleaned_post_url = clean_post_id(post_url)
    if cleaned_post_url not in post_list:
        post_list.append(cleaned_post_url)


def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com")
    email_field = driver.find_element_by_id("email")
    email_field.send_keys(email)
    password_field = driver.find_element_by_id("pass")
    password_field.send_keys(password)
    login_button = driver.find_element_by_css_selector('button[name="login"]')
    login_button.click()
    time.sleep(5)


def scrape_posts(driver, page_url, post_limit):
    login_to_facebook(driver, "adress email", "password")
    driver.get(page_url)
    post_urls = []

    while len(post_urls) < post_limit:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        post_links = driver.find_elements_by_css_selector("[href*=\"posts/\"]")
        for post_link in post_links:
            post_url = post_link.get_attribute("href")
            check_and_add_post_id(post_url, post_urls)

    return post_urls


def save_to_text_files(post_urls):
    batch_size = 250

    for i in range(4):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(post_urls))

        with open(f"batch{i + 1}.txt", "w") as f:
            for post_url in post_urls[start_idx:end_idx]:
                f.write(post_url + "\n")


chrome_driver_path = "C:\\Windows\\System32\\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)

page_url = "https://www.facebook.com/BanqueZitouna"
post_limit = 1000

post_urls = scrape_posts(driver, page_url, post_limit)
save_post_urls_to_text_files(post_urls)

client = MongoClient("mongodb://localhost:27017/")
db = client['mydatabase']
collection = db['post urls for Zitouna']
for post_url in post_urls:
    post_data = {
        'post_id': post_url,
        'scraped_time': datetime.now()
    }
    collection.insert_one(post_data)

driver.quit()

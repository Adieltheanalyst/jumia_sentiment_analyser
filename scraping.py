import random
import sqlite3

import scrapy
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException, TimeoutException, WebDriverException

chrome_options=Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remove-debugging-port-9222")

def start_driver():
    chrome_driver_path = r"C:\Users\gacha\Downloads\chromedriver-win64 (5)\chromedriver-win64\chromedriver.exe"
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service)
driver=start_driver()
with open(r"localurls/output.json","r") as f:
    urls=json.load(f)

extracted_data=[]
invalid_urls=[]
def product_data():
    global extracted_data
    try:
        product_name=driver.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "-fs20", " " )) and contains(concat( " ", @class, " " ), concat( " ", "-pbxs", " " ))]').text.strip()
    except:
        product_name=None

    try:
        price_element=driver.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "-fs24", " " ))]')
        price_text=price_element.text
        price=re.sub(r'[^\d]','',price_text)
        price=int(price)
    except:
        price=None

    try:
        ratings=driver.find_element(By.CSS_SELECTOR ,'.-yl5 .-b').text.strip()
    except:
        ratings=None

    try:
        discount=driver.find_element(By.CSS_SELECTOR,".-dif .-mls").text.strip()
    except:
        discount="0"

    try:
        brand=driver.find_element(By.XPATH,'//div[contains(concat( " ", @class, " " ), concat( " ", "-phs", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "_more", " " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]').text.strip()
    except:
        brand=None
    try:
        raw_text=driver.find_element(By.CSS_SELECTOR,'.-plxs').text
        match=re.search(r'\((\d+)', raw_text)
        number_of_reviews= int(match.group(1)) if match else None
    except:
        number_of_reviews=None

    return {
        "Product_name":product_name,
        "Price":price,
        "ratings":ratings,
        "discount":discount,
        "brand":brand,
        "number_of_reviews":number_of_reviews
    }
# product_data()
# time.sleep(60)
# print(extracted_data)
# driver.find_element(By.XPATH,'//*[@id="pop"]/div/section/button/svg/use').click()
# time.sleep(5)



# time.sleep(10)
# wait = WebDriverWait(driver, 10)
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.-plxs._more")))
# button.click()
#
def close_popup():
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.cls[aria-label='newsletter_popup_close-cta'], .popup-close, button[aria-label='Close']"))
        )
        close_button.click()
        print("Popup closed.")
        time.sleep(1)  # Brief pause after closing popup
    except TimeoutException:
        print("No popup appeared")

def reviews_data():
    review_list=[]
    time.sleep(5)
    close_popup()
    while True:
        reviews = driver.find_elements(By.CSS_SELECTOR, "._bet")
        for review in reviews:
            try:
                review_about=review.find_element(By.CSS_SELECTOR,".-fs16.-pvs").text.strip()
            except:
                review_about=None
            try:
                sentiment=review.find_element(By.CSS_SELECTOR,"p.-pvs").text.strip()
            except:
                sentiment=None
            try:
                raw_rating=review.find_element(By.CSS_SELECTOR,"._al").text.strip()
                star_rating=raw_rating.split(" ")[0]
            except:
                star_rating=None
            try:
                date=review.find_element(By.CSS_SELECTOR,".-pvs .-prs").text.strip()
            except:
                date=None
            review_list.append({
                "Review about": review_about,
                "Sentiment":sentiment,
                "Star_rating": star_rating,
                "Date":date
            })
            time.sleep(5)
        try:
            close_popup()
            next_button=WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//a[@aria-label='Next Page']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            time.sleep(5)
            class_attr=next_button.get_attribute("class")
            if "disabled" in class_attr or not next_button.is_enabled():
                print("No more pages")
                break
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next Page']"))
            )
            next_button.click()
            print("Clicked Next Button")
            time.sleep(5)
        except ElementClickInterceptedException as e:
            print(f"Click intercepted: {e}")
            # Save page source for debugging
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved for debugging")
            break
        except NoSuchElementException:
            print("Next button not found. Probably last page")
            break
        except TimeoutException:
            print("Next button not clickable within timeout")
            break
    return review_list

def save_to_database(product_data,reviews_data):
    conn=sqlite3.connect("jumia_data.db")
    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price INTEGER,
            ratings TEXT,
            discount TEXT,
            brand TEXT,
            number_of_reviews INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            review_about TEXT,
            sentiment TEXT,
            star_rating TEXT,
            date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    cursor.execute("""
        INSERT INTO products (product_name, price, ratings, discount, brand, number_of_reviews)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_data["Product_name"],
        product_data["Price"],
        product_data["ratings"],
        product_data["discount"],
        product_data["brand"],
        product_data["number_of_reviews"]
    ))

    product_id=cursor.lastrowid

    for review in reviews_data:
        cursor.execute("""
            INSERT INTO reviews (product_id, review_about, sentiment, star_rating, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_id,
            review.get("Review about"),
            review.get("Sentiment"),
            review.get("Star_rating"),
            review.get("Date")
        ))
    conn.commit()
    conn.close()

for i , item in enumerate(urls):
    url=item.get("url")
    print(f"Processing link number: {i} --> {url}")

    retry_count=0

    while retry_count < 3 :
        try:
            driver.get(url)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            try:
                server_busy_msg = driver.find_elements(By.XPATH,
                                                       "//pre[contains(text(), 'Server is temporarily unavailable')]")
                if server_busy_msg:
                    print(f"⚠️ Server busy (503): {url} - Waiting 10 minutes before retrying...")
                    time.sleep(600)
                    continue
            except NoSuchElementException:
                pass

            try:
                driver.find_element(By.XPATH, "//h1[contains(text(), 'Page Not Found')]")
                print(f"❌ Page Not Found: {url}")
                invalid_urls.append(url)
                break  # Move to the next URL
            except NoSuchElementException:
                pass
            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cls[aria-label='newsletter_popup_close-cta']"))
                )
                close_button.click()
                print("Popup closed.")
            except:
                print("No popup appeared")
            prod_data=product_data()
            time.sleep(random.randint(3,9))
            try:
                wait = WebDriverWait(driver, 10)
                button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.-plxs._more")))
                button.click()
            except:
                print("Data not Found")
            rev_data=reviews_data()
            # print(prod_data,rev_data)
            save_to_database(prod_data,rev_data)
            wait_time=random.randint(5,20)
            print(f"waiting {wait_time} seconds before the next URL....")
            time.sleep(wait_time)
            break

        except TimeoutException:
            print(f" Timeout on {url}, retrying...")
            retry_count += 1

        except WebDriverException as e:
            print(f"❌ WebDriver disconnected. Restarting driver... Error: {e}")
            driver.quit()
            time.sleep(5)
            driver = start_driver()
            retry_count += 1

        except Exception as e:
            print(f"⚠️ Error processing {url}: {e}")
            invalid_urls.append(url)
            break


if invalid_urls:
    with open("invalid_urls.json","w") as f:
        json.dump(invalid_urls,f,indent=4)
    print(f"📌 Saved {len(invalid_urls)} invalid URLs to invalid_urls.json")





time.sleep(10)
driver.quit()
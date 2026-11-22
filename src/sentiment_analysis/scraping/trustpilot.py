from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from bs4 import BeautifulSoup
import re

sys.stdout.reconfigure(encoding='utf-8')

URL = "https://www.trustpilot.com/review/www.fashionnova.com?page=1"
MAX_REVIEWS = 100

def init_driver():
    options = Options()
    # options.add_argument("--headless")  # اگر لازم بود بدون نمایش مرورگر
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 900)
    return driver

def scroll_to_bottom(driver):
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(0.15)
    # کمی صبر برای بارگذاری محتوا
    time.sleep(2)

def remove_ads(driver):
    try:
        # منتظر می‌مونیم تبلیغ بیاد (تا 5 ثانیه)
        ad_present = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[data-consent-banner], iframe[src*="ads"], div[class*="popup"], div[class*="modal"]'
            ))
        )
        driver.execute_script("""
            const ads = document.querySelectorAll('div[data-consent-banner], iframe[src*="ads"], div[class*="popup"], div[class*="modal"]');
            ads.forEach(ad => ad.remove());
        """)
        print("✅ تبلیغات حذف شد.")
    except:
        print("⚠️ تبلیغی مشاهده نشد یا زودتر حذف شده بود.")

def parse_reviews(driver):

    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = []

    cards = soup.find_all("article", attrs={"data-service-review-card-paper": True})
    for card in cards:
        try:
            # --- نام کاربر ---
            name_tag = card.select_one("span.typography_heading-xxs__...")  # باید دقیق ببینیم
            name = name_tag.get_text(strip=True) if name_tag else ""

            # --- تاریخ ---
            date_tag = card.select_one("time")
            date = date_tag.get_text(strip=True) if date_tag else ""

            # --- ستاره‌ها ---
            stars = 0
            stars_tag = card.select_one("img[alt*='Rated']")
            if stars_tag:
                alt_text = stars_tag.get("alt", "")
                match = re.search(r"Rated\s+(\d+)", alt_text)
                if match:
                    stars = int(match.group(1))

            # --- متن نظر ---
            comment_tag = card.select_one("p[data-service-review-text-typography]")
            comment = comment_tag.get_text(" ", strip=True) if comment_tag else ""

            reviews.append({
                "name": name,
                "date": date,
                "stars": stars,
                "comment": comment
            })
        except Exception as e:
            print("⚠️ خطا در parse کارت:", e)
            continue

    return reviews

def click_next_page(driver):
    try:
        wait = WebDriverWait(driver, 5)  # کوتاه‌تر کردیم
        next_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[name="pagination-button-next"][aria-label="Next page"]')
        ))
        next_btn.click()
        time.sleep(3)  # صبر کمتر برای لود صفحه
        return True
    except:
        return False

def main():
    driver = init_driver()
    print("🔍 باز کردن صفحه اصلی...")
    driver.get(URL)
    time.sleep(3)
    remove_ads(driver)

    all_reviews = []
    page = 1

    while True:
        print(f"\n📄 پردازش صفحه {page} ...")
        scroll_to_bottom(driver)
        remove_ads(driver)
        reviews = parse_reviews(driver)
        print(f"📝 تعداد نظرات این صفحه: {len(reviews)}")
        all_reviews.extend(reviews)

        print(f"💡 جمع کل نظرات: {len(all_reviews)} / {MAX_REVIEWS}")
        if len(all_reviews) >= MAX_REVIEWS:
            print("🎯 به حد نصاب نظرات رسیدیم. پایان کار.")
            break

        if not click_next_page(driver):
            print("⛔ صفحه بعدی وجود ندارد یا دکمه قابل کلیک نیست.")
            break

        page += 1

    if all_reviews:
        df = pd.DataFrame(all_reviews[:MAX_REVIEWS])
        df.to_csv("trustpilot_fashionnova_reviews.csv", index=False, encoding="utf-8-sig")
        print(f"💾 نتایج ذخیره شدند در trustpilot_fashionnova_reviews.csv")
    else:
        print("⚠️ هیچ نظری استخراج نشد!")

    driver.quit()

if __name__ == "__main__":
    main()

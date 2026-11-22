# scraper_basalam_by_steps_all.py
# -*- coding: utf-8 -*-
import sys
import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

MAIN_PAGE_URL = "https://basalam.com/razmishop/product/7005960"
OUTPUT_CSV = "data/raw_reviews_all.csv"

STEP_PIXELS = 650
MAX_STEPS = 200
WAIT_AFTER_SCROLL = 3.0
WAIT_FOR_STYLE_TIMEOUT = 12

def init_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,1024")
    return webdriver.Chrome(options=opts)

def open_comments_modal(driver, url):
    print("🔍 باز کردن صفحه محصول...")
    driver.get(url)
    time.sleep(3)
    btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'تجربه خریدها')]"))
    )
    driver.execute_script("arguments[0].click();", btn)
    print("✅ روی دکمه 'تجربه خریدها' کلیک شد.")
    modal = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bs-modal__content"))
    )
    print("✅ مودال نظرات باز شد.")
    comments_section = WebDriverWait(modal, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.bs-box.GSBwLT"))
    )
    print("✅ بخش نظرات داخل مودال پیدا شد.")
    return comments_section

def find_scroll_element(comments_section):
    candidates = comments_section.find_elements(By.CSS_SELECTOR, 'div[data-testid="virtuoso-scroller"]')
    if candidates:
        return candidates[0]
    all_divs = comments_section.find_elements(By.TAG_NAME, "div")
    for d in all_divs:
        style = (d.get_attribute("style") or "")
        if "overflow-y" in style or "padding-top" in style:
            return d
    raise RuntimeError("اسکرول دیو پیدا نشد.")

def get_padding_top_from_element(el):
    style = el.get_attribute("style") or ""
    m = re.search(r'padding-top\s*:\s*([0-9]+)\s*px', style)
    if m:
        return int(m.group(1))
    try:
        first_child = el.find_element(By.XPATH, "./*")
        style2 = first_child.get_attribute("style") or ""
        m2 = re.search(r'padding-top\s*:\s*([0-9]+)\s*px', style2)
        if m2:
            return int(m2.group(1))
    except:
        pass
    return None

def wait_for_padding_increase(scroll_el, prev_padding, timeout=WAIT_FOR_STYLE_TIMEOUT):
    start = time.time()
    while time.time() - start < timeout:
        cur = get_padding_top_from_element(scroll_el)
        if cur is not None and prev_padding is not None and cur > prev_padding:
            return cur
        if cur is not None and prev_padding is None:
            return cur
        time.sleep(0.5)
    return None

def collect_new_reviews(comments_section, seen_ids):
    review_elements = comments_section.find_elements(By.CSS_SELECTOR, "div.eN63l8._9ltxo8")
    new_items = []
    for r in review_elements:
        rid = r.get_attribute("id") or r.get_attribute("data-item-index") or r.get_attribute("data-index") or None
        if not rid:
            rid = f"noid-{hash(r.text) & 0xfffffff}"
        if rid in seen_ids:
            continue
        seen_ids.add(rid)
        try:
            name = r.find_element(By.CLASS_NAME, "Rqze5j").text.strip()
        except:
            name = ""
        try:
            date = r.find_element(By.CLASS_NAME, "eN4XZm").text.strip()
        except:
            date = ""
        try:
            stars = len(r.find_elements(By.CLASS_NAME, "bs-rating__star--active"))
        except:
            stars = 0
        try:
            text = r.find_element(By.CLASS_NAME, "nkJy9o").text.strip()
        except:
            text = ""
        new_items.append({
            "id": rid,
            "نام کاربر": name,
            "تاریخ": date,
            "امتیاز": stars,
            "متن نظر": text
        })
    return new_items, len(review_elements)

WAIT_AFTER_SCROLL = 0.1
WAIT_FOR_STYLE_TIMEOUT = 1.0

def scrape_all_reviews(driver, comments_section, step_pixels=STEP_PIXELS):
    scroll_el = find_scroll_element(comments_section)
    print("✅ اسکرولر پیدا شد و آمادهٔ اسکرول مرحله‌ای است.")

    seen = set()
    all_reviews = []
    no_new_count = 0

    initial_new, total_now = collect_new_reviews(comments_section, seen)
    if initial_new:
        print(f"⏺ ابتدا {len(initial_new)} مورد جدید یافت شد.")
        all_reviews.extend(initial_new)
    else:
        print(f"⏺ ابتدا هیچ مورد جدیدی یافت نشد (total_now={total_now}).")

    step = 0
    prev_padding = get_padding_top_from_element(scroll_el)
    print(f"🔢 padding-top شروع: {prev_padding}")

    while step < MAX_STEPS:
        step += 1
        print(f"\n--- گام {step} — اسکرول {step_pixels}px ---")
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];",
            scroll_el, step_pixels
        )
        time.sleep(0.25)

        new_padding = wait_for_padding_increase(scroll_el, prev_padding, timeout=3)
        if new_padding is None:
            print("⚠️ padding-top تغییر نکرد (timeout). تلاش بعدی.")
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];",
                scroll_el, step_pixels
            )
            time.sleep(0.6)
            new_padding = get_padding_top_from_element(scroll_el)
        else:
            print(f"✅ padding-top تغییر کرد: {prev_padding} -> {new_padding}")

        prev_padding = new_padding if new_padding is not None else prev_padding
        time.sleep(0.6)

        new_items, total_now = collect_new_reviews(comments_section, seen)
        if new_items:
            print(f"➕ {len(new_items)} نظر جدید اضافه شد (کل الان: {len(all_reviews) + len(new_items)})")
            all_reviews.extend(new_items)
            no_new_count = 0
        else:
            print("➖ مورد جدیدی پیدا نشد در این گام.")
            no_new_count += 1
            if no_new_count >= 2:
                print("⏹ دو بار متوالی مورد جدیدی پیدا نشد. توقف اسکرول.")
                break

        print(f"🔢 تعداد کلی لود شده در DOM: {total_now}, جمع نهایی فعلی: {len(all_reviews)}")

    print("\n✅ پایان اسکرول مرحله‌ای.")
    return pd.DataFrame(all_reviews)

def main():
    os.makedirs("data", exist_ok=True)
    driver = init_driver(headless=False)
    try:
        comments_section = open_comments_modal(driver, MAIN_PAGE_URL)
        df = scrape_all_reviews(driver, comments_section, step_pixels=STEP_PIXELS)
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"\n💾 فایل ذخیره شد در: {OUTPUT_CSV}, تعداد: {len(df)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

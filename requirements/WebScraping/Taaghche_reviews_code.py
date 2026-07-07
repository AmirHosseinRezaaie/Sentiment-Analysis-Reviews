# بخش اول: ورود به صفحه نظرات از صفحه اصلی 

# کتابخانه‌های مورد نیاز را وارد می‌کنیم

# برای مدیریت تنظیمات سیستم‌عامل و پیکربندی خروجی‌ها
import sys

# برای ایجاد تاخیرهای زمانی در اجرای کد
import time

# برای ذخیره اطلاعات به صورت فایل CSV
import pandas as pd

# برای پردازش و تجزیه کد HTML
from bs4 import BeautifulSoup

# برای کنترل مرورگر با استفاده از Selenium
from selenium import webdriver

# برای تنظیمات مرورگر مانند هدلس بودن، غیرفعال‌سازی گرافیک و غیره
from selenium.webdriver.chrome.options import Options

# برای انتخاب عناصر HTML با استفاده از نوع مکان‌یابی
from selenium.webdriver.common.by import By

# برای منتظر ماندن تا زمانی که یک عنصر خاص آماده شود
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# برای شبیه‌سازی حرکت موس و کلیک (در صورتی که کلیک ساده کار نکند)
from selenium.webdriver.common.action_chains import ActionChains

import os

# رفع مشکل نمایش حروف فارسی در خروجی‌های سیستم عامل ویندوز
sys.stdout.reconfigure(encoding='utf-8')

# آدرس صفحه کتاب (می‌توانید این آدرس را تغییر دهید)
MAIN_PAGE_URL = "https://taaghche.com/book/503/%D9%85%D8%A7%D9%87%DB%8C-%D8%B3%DB%8C%D8%A7%D9%87-%DA%A9%D9%88%DA%86%D9%88%D9%84%D9%88"

# تنظیمات مرورگر برای بخش اول - در این قسمت مرورگر واقعی نمایش داده می‌شود
main_options = Options()
# چون می‌خواهیم مرورگر دیده شود، هدلس نمی‌گذاریم

# ساخت مرورگر کروم با تنظیمات بالا
main_driver = webdriver.Chrome(options=main_options)
# تنظیم اندازه پنجره مرورگر
main_driver.set_window_size(1280, 1024)

# باز کردن صفحه اصلی کتاب
print("در حال بارگذاری مرورگر و صفحه اصلی کتاب...")
main_driver.get(MAIN_PAGE_URL)
time.sleep(2)

# اسکرول به پایین برای نمایش بخش نظرات
for _ in range(25):
    main_driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(0.3)
    try:
        if main_driver.find_element(By.CLASS_NAME, "commentBox_header__mYVFx").is_displayed():
            print("✅ به بخش نظرات رسیدیم.")
            break
    except:
        pass

# ذخیره آدرس فعلی برای بررسی تغییرات پس از کلیک
original_url = main_driver.current_url
clicked = False

# تلاش برای یافتن دکمه نمایش همه نظرات
try:
    button = main_driver.find_element(By.CSS_SELECTOR, "div.commentBox_headerMore__RblUv span.d-none.d-sm-block")
    print("🔍 دکمه مشاهده همه نظرات پیدا شد.")
except:
    print("🚫دکمه مشاهده نظرات پیدا نشد.")
    main_driver.quit()
    exit()

# روش اول: کلیک ساده
try:
    button.click()
    time.sleep(2)
    if main_driver.current_url != original_url:
        print("✅کلیک ساده موفق بود.")
        clicked = True
    else:
        print("کلیک انجام شد ولی وارد بخش نظرات نشد.❌")
except Exception as e:
    print(f"کلیک ساده شکست خورد: {e}❌")

# روش دوم: کلیک با ActionChains
if not clicked:
    try:
        ActionChains(main_driver).move_to_element(button).click().perform()
        time.sleep(2)
        if main_driver.current_url != original_url:
            print("کلیک با روش ActionChains موفق بود.✅")
            clicked = True
        else:
            print("کلیک ActionChains انجام شد ولی وارد بخش نظرات نشد.❌")
    except Exception as e:
        print(f"کلیک ActionChains ❌شکست خورد: {e}")

# روش سوم: کلیک با جاوااسکریپت
if not clicked:
    try:
        main_driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        if main_driver.current_url != original_url:
            print("کلیک با جاوااسکریپت موفق بود.✅")
            clicked = True
        else:
            print("کلیک جاوااسکریپتی انجام شد ولی وارد بخش نظرات نشد.❌")
    except Exception as e:
        print(f"❌کلیک جاوااسکریپت شکست خورد: {e}")

# روش چهارم: اجرای مستقیم اسکریپت جاوااسکریپت
if not clicked:
    try:
        js_script = """
        let btn = document.querySelector('div.commentBox_headerMore__RblUv span.d-none.d-sm-block');
        if (btn) btn.click();
        """
        main_driver.execute_script(js_script)
        time.sleep(2)
        if main_driver.current_url != original_url:
            print("کلیک مستقیم جاوااسکریپتی موفق بود.✅")
            clicked = True
        else:
            print("کلیک جاوااسکریپتی انجام شد ولی صفحه تغییر نکرد.❌")
    except Exception as e:
        print(f"اجرای جاوااسکریپت شکست خورد: {e}")

# اگر کلیک موفق بود، لینک صفحه نظرات را دریافت کن
if clicked:
    comments_url = main_driver.current_url
    print(f"🎯 کلیک موفق! وارد لینک نظرات شدیم: {comments_url}")
else:
    print("هیچ‌کدام از روش‌ها باعث ورود به صفحه نظرات نشد.⛔")
    main_driver.quit()
    exit()

# بستن مرورگر
main_driver.quit()
print("مرورگر بسته شد. استخراج اطلاعات نظرات بلافاصله آغاز خواهد شد...")

#بخش دوم: استخراج تمام نظرات

# تابع برای بستن بنر تبلیغ اپلیکیشن طاقچه در صورت نمایش
def close_install_banner():
    try:
        close_btn = driver.find_element(By.CLASS_NAME, "installBox_closeButton__wUhrd")
        close_btn.click()
        time.sleep(1)
    except:
        pass  # اگر دکمه پیدا نشد، نادیده بگیر

# آدرس صفحه نظرات کتاب که از مرحله قبل به دست آمده
BOOK_URL = comments_url

# تنظیمات مرورگر به صورت headless (بدون نمایش مرورگر برای افزایش سرعت)
options = Options()

# این گزینه مرورگر را به صورت بدون واسط گرافیکی اجرا می‌کند (یعنی صفحه باز نمی‌شود)
options.add_argument("--headless")

# این گزینه محدودیت‌های امنیتی سیستم‌عامل را غیرفعال می‌کند (برای اجرای روان‌تر در برخی سیستم‌ها)
options.add_argument("--no-sandbox")

# این گزینه از استفاده بیش از حد حافظه مشترک جلوگیری می‌کند (برای جلوگیری از خطا در برخی سیستم‌ها)
options.add_argument("--disable-dev-shm-usage")

# راه‌اندازی مرورگر با تنظیمات بالا
driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 1024)  # تنظیم اندازه پنجره به‌صورت استاندارد
driver.get(BOOK_URL)
time.sleep(3)  # تاخیر برای بارگذاری کامل صفحه

# شمارنده تعداد کلیک‌ها روی دکمه «مشاهده بیشتر نظرات»
click_attempts = 0

# مقدار اولیه برای بررسی تغییر در تعداد نظرات
previous_loaded_comments = 0

# حلقه‌ای برای کلیک پشت‌سرهم روی دکمه "نمایش نظرات بیشتر"
while True:
    try:
        # بستن احتمالی بنر تبلیغاتی
        close_install_banner()

        # صبر تا زمانی که دکمه نمایش بیشتر آماده کلیک شود
        wait = WebDriverWait(driver, 5)
        more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bookComments_moreButton__1xrpL")))

        # دوباره تلاش برای بستن بنر اگر دوباره ظاهر شد
        close_install_banner()

        # کلیک روی دکمه برای نمایش نظرات بیشتر
        more_button.click()
        click_attempts += 1
        time.sleep(2.5)

        # بررسی تعداد نظرات بارگذاری‌شده پس از هر کلیک
        page_html = driver.page_source
        soup_temp = BeautifulSoup(page_html, "html.parser")
        all_comments = soup_temp.find_all("div", class_="bookComments_comment___TU8v")
        loaded_comments = len(all_comments)

        print(f"✅ کلیک {click_attempts}: نظرات تا این لحظه {loaded_comments}")

        # اگر تعداد نظرات نسبت به مرحله قبل تغییری نداشته باشد، حلقه را متوقف کن
        if loaded_comments == previous_loaded_comments:
            print("🚫 تعداد نظرات جدیدی بارگذاری نشد. کلیک متوقف شد.")
            break

        # به‌روزرسانی تعداد نظرات قبلی برای مقایسه در مرحله بعد
        previous_loaded_comments = loaded_comments

    except Exception as e:
        print(f"بارگذاری نظرات کامل شد یا مشکلی در کلیک وجود دارد: {e}")
        break  # پایان حلقه در صورت خطا یا تمام‌شدن دکمه

# پس از اتمام بارگذاری نظرات، صفحه کامل HTML را می‌گیریم
html = driver.page_source

# بستن مرورگر پس از پایان کار
driver.quit()

# پیام مشخص برای اتمام مرحله استخراج از مرورگر
print("مرورگر بسته شد. اکنون داده‌ها آماده پردازش نهایی هستند...")

# شروع پردازش HTML و استخراج اطلاعات نظرات
soup = BeautifulSoup(html, "html.parser")

# پیدا کردن بخش نظرات اصلی در صفحه
all_comments_div = soup.find("div", class_="bookComments_comments__rhkoN")

# استخراج تمام بلوک‌های نظر
comment_blocks = all_comments_div.find_all("div", class_="bookComments_comment___TU8v", recursive=True)

# فهرست برای ذخیره اطلاعات نهایی نظرات
comments_data = []

# شمارنده برای تعداد نظرات اصلی (پاسخ‌ها را شامل نمی‌شود)
real_count = 0

# پردازش تک‌تک نظرات
for block in comment_blocks:
    # حذف پاسخ‌ها؛ فقط نظرات اصلی را نگه می‌داریم
    if block.find_parent("div", class_="bookComments_replies__dXS_n"):
        continue

    try:
        info_div = block.find("div", class_="bookComments_info__7AZzG")
        inner_divs = info_div.find_all("div")

        if len(inner_divs) < 2:
            continue  # اگر ساختار ناقص بود، رد شو

        name_stars_container = inner_divs[1]
        name_div = name_stars_container.find_all("div")[0]
        stars_div = name_stars_container.find_all("div")[1]
        star_spans = stars_div.find_all("span", class_="icon-star-2")

        name = name_div.text.strip()  # نام کاربر
        stars = len(star_spans)       # تعداد ستاره‌ها

        content_div = block.find("div", class_="bookComments_content___9Xbz")
        comment_text = content_div.text.strip()  # متن نظر

        # ذخیره اطلاعات استخراج‌شده در لیست نهایی
        comments_data.append({
            "name": name,
            "stars": stars,
            "comment": comment_text
        })

        real_count += 1

    except Exception as e:
        print("🚫خطا در پردازش یک نظر:", e)

# ذخیره اطلاعات نظرات در فایل CSV
comments_df = pd.DataFrame(comments_data)
# ساخت مسیر پوشه data/Taghche در صورت نبود
save_dir = os.path.join("data", "Taghche")
os.makedirs(save_dir, exist_ok=True)

# مسیر کامل فایل خروجی
save_path = os.path.join(save_dir, "taaghche_reviews_MSK.csv")

# ذخیره فایل CSV در مسیر تعیین‌شده
comments_df.to_csv(save_path, index=False, encoding="utf-8-sig")

print(f"✅ فایل ذخیره شد: {save_path} (تعداد کل نظرات: {len(comments_data)})")


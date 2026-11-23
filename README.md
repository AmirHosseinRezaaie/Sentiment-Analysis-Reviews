# تحلیل احساسات نظرات | Sentiment Analysis Reviews

پروژه‌ای پژوهشی برای بررسی یک جریان کامل تحلیل احساسات روی دیدگاه‌های کاربران: از جمع‌آوری داده از وب‌سایت‌ها تا پردازش زبان طبیعی، آموزش مدل‌های یادگیری ماشین و ارزیابی نتایج.

این مخزن در ابتدا به شکل چند نوت‌بوک مستقل توسعه داده شده است. ساختار فعلی مسئولیت هر حوزه را جدا می‌کند و نوت‌بوک‌ها و خروجی‌های تاریخی را برای بررسی و بازتولید آزمایش‌ها نگه می‌دارد.

## نقشه پروژه

```text
SentimentProject/
├── app/                         # نقطه ورود و رابط خط فرمان پروژه
│   └── main.py
├── src/
│   └── sentiment_analysis/
│       ├── scraping/             # استخراج داده از وب‌سایت‌ها
│       └── preprocessing/        # کدهای قدیمی پیش‌پردازش متن
├── notebooks/
│   └── experiments/              # آزمایش‌های کامل هر منبع داده
├── data/                         # داده‌های خام و پاک‌سازی‌شده، به تفکیک منبع
│   ├── basalam/
│   ├── Taaghche/
│   └── trustpilot/
├── models/                       # مدل‌های ذخیره‌شده و جدول مقایسه
├── figures/                      # نمودارهای EDA و ماتریس‌های درهم‌ریختگی
├── files/                        # مجموعه‌های train/test و منابع جانبی
├── reports/                      # گزارش نهایی PDF و DOCX
├── requirements-core.txt         # وابستگی‌های پایه تحلیل و نوت‌بوک
├── requirements-scraping.txt     # وابستگی‌های وب‌اسکرپینگ
├── requirements-persian.txt      # وابستگی‌های NLP فارسی
└── pyproject.toml                # مشخصات نصب و فرمان پروژه
```

## حوزه‌های فنی

| حوزه | محل | مسئولیت |
|---|---|---|
| Web Scraping | `src/sentiment_analysis/scraping/` | جمع‌آوری دیدگاه از Basalam، Taaghche و Trustpilot با Selenium و BeautifulSoup |
| NLP و پیش‌پردازش | `src/sentiment_analysis/preprocessing/` و نوت‌بوک‌ها | پاک‌سازی متن، نرمال‌سازی، حذف stop words و آماده‌سازی داده فارسی و انگلیسی |
| EDA و مصورسازی | نوت‌بوک‌ها و `figures/` | بررسی توزیع برچسب‌ها، طول دیدگاه‌ها، Word Cloud و نمودارهای تحلیلی |
| Feature Engineering | نوت‌بوک‌ها | تبدیل متن به ویژگی‌های عددی با TF-IDF و n-gram |
| Machine Learning | نوت‌بوک‌ها و `models/` | آزمایش Multinomial Naive Bayes، Logistic Regression و Linear SVM |
| Evaluation | نوت‌بوک‌ها، `models/model_comparison.csv` و `figures/` | بررسی Accuracy، Precision، Recall، F1 و Confusion Matrix |
| گزارش‌دهی | `reports/` | نگهداری گزارش مکتوب پروژه |
| رابط اجرا | `app/` | دسترسی یکپارچه به آزمایش‌ها و اسکریپت‌های استخراج از خط فرمان |

## جریان داده

```text
وب‌سایت‌ها
    │
    ▼
Web Scraping (src/sentiment_analysis/scraping)
    │
    ▼
داده خام (data/<source>/)
    │
    ▼
NLP / Text Preprocessing
    │
    ▼
داده پاک‌سازی‌شده و برچسب‌خورده
    │
    ▼
EDA → TF-IDF → Train / Test
    │
    ▼
Naive Bayes / Logistic Regression / Linear SVM
    │
    ▼
Evaluation → models/ + figures/ + reports/
```

نوت‌بوک‌ها مسیرهای داده و خروجی را از ریشه مخزن می‌خوانند. به همین دلیل هنگام اجرای آن‌ها، ریشه پروژه به عنوان working directory تنظیم می‌شود و پوشه‌های `data/`، `models/`، `figures/` و `files/` در ریشه باقی مانده‌اند.

## شروع سریع

Python 3.9 یا جدیدتر پیشنهاد می‌شود. ابتدا محیط مجازی بسازید و وابستگی‌های موردنیاز خود را نصب کنید:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements-core.txt
```

برای اجرای استخراج داده، وابستگی scraping را هم نصب کنید:

```bash
pip install -r requirements-scraping.txt
```

برای ابزارهای پردازش زبان فارسی:

```bash
pip install -r requirements-persian.txt
```

نمای کلی فرمان‌ها:

```bash
python -m app.main overview
```

اجرای نوت‌بوک هر منبع:

```bash
python -m app.main notebook basalam
python -m app.main notebook taaghche
python -m app.main notebook trustpilot
```

اجرای scraper هر وب‌سایت:

```bash
python -m app.main scrape basalam
python -m app.main scrape taaghche
python -m app.main scrape trustpilot
```

### استخراج نظرات با لینک دلخواه

برای استخراج از هر محصول باسلام، هر کتاب طاقچه یا هر صفحه شرکت در Trustpilot، کافی است لینک صفحه را به مدیر مرکزی بدهید. مدیر دامنه را تشخیص می‌دهد و scraper مناسب را اجرا می‌کند:

```bash
# ورود تعاملی لینک
python -m app.main scrape-url

# ارسال مستقیم لینک
python -m app.main scrape-url "https://basalam.com/shop/product/123"
python -m app.main scrape-url "https://taaghche.com/book/123/book-title" --headless
python -m app.main scrape-url "https://www.trustpilot.com/review/example.com" --output data/trustpilot/example.csv
```

برای اجرای مستقیم مدیر استخراج نیز می‌توانید از این فرمان استفاده کنید:

```bash
python -m src.sentiment_analysis.scraping.manager
```

در مسیرهای جدید استخراج، سقف ثابتی برای تعداد نظرات تعریف نشده است. جمع‌آوری تا پایان صفحه‌بندی سایت یا تشخیص پایدار انتهای فهرست ادامه پیدا می‌کند. تعداد واقعی نظرات قابل دریافت همچنان به محتوایی که خود وب‌سایت در اختیار مرورگر قرار می‌دهد، دسترسی حساب/منطقه و محدودیت‌های سایت وابسته است. اگر ساختار HTML یا selectorهای سایت تغییر کند، باید parser همان سایت به‌روزرسانی شود.

اجرای نوت‌بوک به JupyterLab نیاز دارد. اجرای scraperها به مرورگر Chrome و نسخه سازگار ChromeDriver نیاز دارد. ساختار HTML وب‌سایت‌ها ممکن است تغییر کند و در نتیجه استخراج داده به اصلاح selectorها نیاز پیدا کند.

## داده‌ها و آزمایش‌ها

- `data/` شامل نسخه‌های موجود داده خام و پاک‌سازی‌شده برای سه منبع است.
- `notebooks/experiments/` روند آزمایش هر منبع را از استخراج تا مدل‌سازی و ارزیابی نگه می‌دارد.
- `models/` شامل فایل‌های مدل و بردارساز ذخیره‌شده با Joblib و جدول مقایسه مدل‌ها است.
- `figures/` شامل نمودارهای تولیدشده در آزمایش‌ها است.
- `files/` شامل نمونه‌های train/test و فایل فونت مورد استفاده در خروجی‌ها است.
- `reports/` گزارش PDF و Word پروژه را نگه می‌دارد.

فایل‌های `.pkl` با `joblib` و نسخه‌های مشخصی از کتابخانه‌های پایتون ساخته شده‌اند؛ بارگذاری آن‌ها با نسخه‌های ناسازگار Scikit-learn ممکن است خطا بدهد. این فایل‌ها را فقط از منبع قابل اعتماد بارگذاری کنید.

## وضعیت فعلی و محدودیت نتایج

این مخزن سابقه آزمایش‌های اولیه را حفظ می‌کند و هنوز یک مدل نهایی و قابل اتکا برای استفاده عملیاتی معرفی نمی‌کند. مقدارهای ثبت‌شده در نوت‌بوک‌ها، جدول مقایسه و گزارش‌ها ممکن است مربوط به اجراها و مجموعه‌داده‌های متفاوت باشند؛ بنابراین نباید آن‌ها را بدون اجرای مجدد و ارزیابی یکسان، نتیجه قطعی پروژه در نظر گرفت.

در بعضی آزمایش‌ها عدم توازن کلاس‌ها و ضعف تشخیص کلاس منفی مشاهده شده است. برای ارزیابی معتبرتر، گام‌های بعدی پروژه می‌تواند شامل جداسازی داده بدون نشت اطلاعات، ساخت Pipeline یکپارچه پیش‌پردازش و مدل، اعتبارسنجی متقاطع، تنظیم آستانه و گزارش Macro-F1 و معیارهای هر کلاس باشد. این موارد مسیر توسعه بعدی هستند و در این بازآرایی به منطق آزمایش‌های قبلی دست زده نشده است.

## مسیر توسعه بعدی

1. استخراج منطق مشترک نوت‌بوک‌ها به ماژول‌های مستقل و قابل استفاده مجدد.
2. تعریف قرارداد داده و schema مشترک برای منابع مختلف.
3. ساخت pipeline آموزش و ارزیابی قابل تکرار با ثبت تنظیمات و نسخه داده.
4. مدیریت نسخه مدل‌ها و ارزیابی روی داده‌های دیده‌نشده.
5. افزودن API و رابط کاربری تعاملی برای تحلیل نظر توسط کاربر.

---

# English Overview

A modular research project for review sentiment analysis across Persian and English sources. It covers web scraping, NLP preprocessing, exploratory analysis, TF-IDF feature extraction, classical machine learning, model evaluation, and reporting.

- **Scraping:** `src/sentiment_analysis/scraping/`
- **NLP / preprocessing:** `src/sentiment_analysis/preprocessing/` and experiment notebooks
- **Experiments:** `notebooks/experiments/`
- **Datasets:** `data/`
- **Trained artifacts:** `models/`
- **Visualizations:** `figures/`
- **Reports:** `reports/`
- **CLI entry point:** `app/main.py`

Run `python -m app.main overview` to see available workflows. Install the relevant requirements file before running notebooks or scrapers. Existing experiments and their outputs are preserved as historical research artifacts; reported metrics should be revalidated on a consistent, leakage-free evaluation setup before being treated as production performance.

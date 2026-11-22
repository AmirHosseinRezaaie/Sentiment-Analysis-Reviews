import os, re, string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from hazm import Normalizer 
from hazm import WordTokenizer

from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ------------------------
# 1. بارگذاری داده
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "..", "data", "raw_reviews.csv")

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"❌ فایل {csv_file} پیدا نشد")

df = pd.read_csv(csv_file, encoding="utf-8-sig")

# ------------------------
# 2. حذف امتیاز 3 و برچسب‌گذاری
# ------------------------
df = df[df['stars'] != 3]
df['sentiment'] = df['stars'].apply(lambda x: 1 if x >= 4 else 0)

# ------------------------
# 3. EDA اولیه
# ------------------------
df['comment_length'] = df['comment'].apply(lambda x: len(str(x).split()))
print(f"میانگین طول دیدگاه‌ها: {df['comment_length'].mean():.2f} 📝")
print(f"کوتاه‌ترین: {df['comment_length'].min()} کلمه ✂️")
print(f"بلندترین: {df['comment_length'].max()} کلمه 📏")

# راست‌چین کردن متن فارسی در نمودار
def fa_text(text):
    try:
        return get_display(arabic_reshaper.reshape(text))
    except:
        return text

plt.figure(figsize=(6,5))
sns.countplot(x='sentiment', data=df, palette="viridis", hue='sentiment', legend=False)
plt.title(fa_text("توزیع احساسات 😃😢"))
plt.xticks([0,1], [fa_text("منفی 😢"), fa_text("مثبت 😃")])
plt.show()

# ------------------------
# 4. پاکسازی متن
# ------------------------
persian_stopwords = list(set([
    'و', 'در', 'به', 'از', 'که', 'می', 'با', 'برای', 'این', 'آن', 'است', 'ها', 'یک', 'بر', 'را', 'شود',
    'هر', 'تا', 'او', 'ما', 'شما', 'آنها', 'هم', 'نیز', 'اما', 'اگر', 'جز', 'نه', 'یا', 'دیگر',
    'مثل', 'فقط', 'پس', 'چون', 'کنید', 'کنند', 'بود', 'شد', 'آنچه', 'یکی', 'ترین',
    'هرگز', 'همه', 'باید', 'نزدیک', 'همین', 'یعنی', 'وقتی', 'خیلی', 'چند', 'اگرچه', 'ولی', 'اند'
]))

normalizer = Normalizer()

# پیش‌پردازش متن
# حذف ایموجی‌ها
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # پرچم‌ها
        "\U0001F300-\U0001F5FF"  # نمادهای عمومی
        "\U0001F600-\U0001F64F"  # شکلک‌ها
        "\U0001F680-\U0001F6FF"  # حمل و نقل
        "\U0001F700-\U0001F77F"  # سمبل‌های دیگر
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\u2600-\u26FF"          # سمبل‌های عمومی
        "\u2700-\u27BF"          # سمبل‌های دیگر
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def preprocess_text(text, for_wordcloud=False):
    if not isinstance(text, str):
        return ""
    text = normalizer.normalize(text)
    text = remove_emojis(text)                        # حذف جامع ایموجی‌ها
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)  # حذف علائم
    text = re.sub(r"\d+", " ", text)                                # حذف عدد
    text = re.sub(r"\s+", " ", text).strip()                        # حذف فاصله اضافه
    tokens = text.split()
    filtered_tokens = [w for w in tokens if w not in persian_stopwords]
    return " ".join(filtered_tokens)


df['processed_comment'] = df['comment'].apply(preprocess_text)

# ------------------------
# 5. WordCloud برای مثبت و منفی
# ------------------------
def reshape_fa_text(text):
    text = ''.join(c for c in text if c.isprintable())
    try:
        return get_display(arabic_reshaper.reshape(text))
    except Exception as e:
        print("⚠️ خطا در reshape:", e)
        return text

pos_text = " ".join(df[df['sentiment'] == 1]['processed_comment'])
neg_text = " ".join(df[df['sentiment'] == 0]['processed_comment'])

if pos_text.strip():
    wc_pos = WordCloud(width=800, height=400, background_color='white').generate(reshape_fa_text(pos_text))
    plt.imshow(wc_pos, interpolation='bilinear')
    plt.axis('off')
    plt.title(fa_text("دیدگاه‌های مثبت 😃"))
    plt.show()

if neg_text.strip():
    wc_neg = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(reshape_fa_text(neg_text))
    plt.imshow(wc_neg, interpolation='bilinear')
    plt.axis('off')
    plt.title(fa_text("دیدگاه‌های منفی 😢"))
    plt.show()

# ------------------------
# 6. پرکاربردترین کلمات
# ------------------------
def top_words(text, n=20):
    words = text.split()
    return Counter(words).most_common(n)

print("پرکاربردترین کلمات مثبت:", top_words(pos_text))
print("پرکاربردترین کلمات منفی:", top_words(neg_text))

# ------------------------
# 7. بردارسازی و SMOTE
# ------------------------
X = df['processed_comment']
y = df['sentiment']
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)
x_train, x_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

print("قبل از SMOTE:", pd.Series(y_train).value_counts())
smote = SMOTE(random_state=42)
x_train_res, y_train_res = smote.fit_resample(x_train, y_train)
print("بعد از SMOTE:", pd.Series(y_train_res).value_counts())

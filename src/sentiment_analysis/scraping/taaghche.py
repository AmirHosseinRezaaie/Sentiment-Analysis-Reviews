"""Taaghche book-review scraper with an import-safe public API."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def _stable_id(name: str, date: str, stars: int | None, comment: str) -> str:
    payload = "|".join((name.strip(), date.strip(), str(stars), comment.strip()))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_review_html(html: str) -> list[dict[str, Any]]:
    """Parse main reviews from a Taaghche comments page (not replies)."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("div[class*='bookComments_comment']")
    reviews: list[dict[str, Any]] = []
    for block in blocks:
        if block.find_parent("div", class_=lambda value: value and any("bookComments_replies" in item for item in (value if isinstance(value, list) else [value]))):
            continue

        info = block.select_one("[class*='bookComments_info']")
        name = ""
        stars: int | None = None
        if info:
            name_node = info.select_one("[class*='name'], [class*='user']")
            if name_node:
                name = name_node.get_text(" ", strip=True)
            else:
                # Fallback to the original layout, but avoid positional access
                # unless the expected elements are actually present.
                containers = info.find_all("div")
                if len(containers) >= 2:
                    inner = containers[1].find_all("div", recursive=False)
                    if inner:
                        name = inner[0].get_text(" ", strip=True)
            stars_node = info.select_one("[class*='star']")
            if stars_node:
                active = stars_node.select(".icon-star-2")
                if active:
                    stars = len(active)
            if stars is None:
                active_stars = info.select("span.icon-star-2")
                if active_stars:
                    stars = len(active_stars)

        date_node = block.select_one("time, [class*='date']")
        date = date_node.get_text(" ", strip=True) if date_node else ""
        content_node = block.select_one("[class*='bookComments_content']")
        comment = content_node.get_text(" ", strip=True) if content_node else ""
        if not (name or date or comment):
            continue
        reviews.append({
            "id": _stable_id(name, date, stars, comment),
            "name": name,
            "date": date,
            "stars": stars,
            "comment": comment,
        })
    return reviews


def _get_comments_url(driver, url: str, wait_seconds: int) -> str:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    driver.get(url)
    # A direct comments URL can be used as input without navigating twice.
    if "comments" in driver.current_url.lower():
        return driver.current_url

    try:
        WebDriverWait(driver, wait_seconds).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "[class*='commentBox_header']")
        )
    except Exception as exc:
        raise RuntimeError("بخش نظرات کتاب در صفحه طاقچه پیدا نشد؛ لینک کتاب را بررسی کنید.") from exc

    links = driver.find_elements(By.CSS_SELECTOR, "[class*='commentBox_headerMore'] a")
    if links:
        href = links[0].get_attribute("href")
        if href:
            return href

    buttons = driver.find_elements(By.CSS_SELECTOR, "[class*='commentBox_headerMore']")
    if not buttons:
        raise RuntimeError("لینک مشاهده همه نظرات در صفحه کتاب پیدا نشد.")
    driver.execute_script("arguments[0].click();", buttons[0])
    WebDriverWait(driver, wait_seconds).until(lambda d: d.current_url != url)
    return driver.current_url


def scrape_reviews(
    url: str,
    *,
    output_path: str | Path | None = None,
    headless: bool = False,
    wait_seconds: int = 15,
) -> "pd.DataFrame":
    """Extract every accessible review; no maximum review count is applied."""
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1024")
    driver = webdriver.Chrome(options=options)
    destination = Path(output_path) if output_path else Path("data/Taaghche") / "reviews.csv"
    collected: dict[str, dict[str, Any]] = {}

    try:
        comments_url = _get_comments_url(driver, url, wait_seconds)
        if driver.current_url != comments_url:
            driver.get(comments_url)
        WebDriverWait(driver, wait_seconds).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "[class*='bookComments_comment']")
        )

        while True:
            page_reviews = parse_review_html(driver.page_source)
            for review in page_reviews:
                collected.setdefault(review["id"], review)

            destination.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(collected.values()).to_csv(destination, index=False, encoding="utf-8-sig")
            LOGGER.info("Taaghche reviews collected: %d", len(collected))

            more_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='bookComments_moreButton']")
            if not more_buttons:
                break
            button = more_buttons[0]
            if not button.is_enabled():
                break
            before = len(driver.find_elements(By.CSS_SELECTOR, "[class*='bookComments_comment']"))
            driver.execute_script("arguments[0].click();", button)
            try:
                WebDriverWait(driver, wait_seconds).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, "[class*='bookComments_comment']")) > before
                )
            except Exception:
                # A still-present button that failed to load more is a failure,
                # not evidence that pagination ended normally.
                still_present = driver.find_elements(By.CSS_SELECTOR, "button[class*='bookComments_moreButton']")
                if still_present and still_present[0].is_enabled():
                    raise RuntimeError("بارگذاری نظرات بیشتر در طاقچه ناموفق بود؛ استخراج ناقص متوقف شد.")
                break

        return pd.DataFrame(collected.values())
    finally:
        driver.quit()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Extract reviews from any Taaghche book URL")
    parser.add_argument("url", nargs="?")
    parser.add_argument("--output")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    url = args.url or input("لینک کتاب یا صفحه نظرات طاقچه را وارد کنید: ").strip()
    frame = scrape_reviews(url, output_path=args.output, headless=args.headless)
    print(f"تعداد نظرات استخراج‌شده: {len(frame)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Trustpilot company-review scraper for arbitrary company review URLs."""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def _stable_id(name: str, date: str, stars: int | None, comment: str) -> str:
    payload = "|".join((name.strip(), date.strip(), str(stars), comment.strip()))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _text(card: Any, selectors: tuple[str, ...]) -> str:
    for selector in selectors:
        node = card.select_one(selector)
        if node:
            value = node.get_text(" ", strip=True)
            if value:
                return value
    return ""


def _rating_from_alt(alt_text: str) -> int | None:
    match = re.search(r"rated\s+(\d+)\s+out\s+of\s+5", alt_text, re.I)
    if not match:
        match = re.search(r"rated\s+(\d+)\b", alt_text, re.I)
    if not match:
        return None
    rating = int(match.group(1))
    return rating if 1 <= rating <= 5 else None


def parse_review_html(html: str) -> list[dict[str, Any]]:
    """Parse review cards and preserve unknown ratings as None, never zero."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("article[data-service-review-card-paper]")
    reviews: list[dict[str, Any]] = []
    for card in cards:
        name = _text(card, (
            "[data-consumer-name-typography]",
            "span[class*='typography_heading-xxs']",
            "a[href*='/users/'] span",
        ))
        date_node = card.select_one("time")
        date = (date_node.get("datetime") or date_node.get_text(" ", strip=True)) if date_node else ""

        stars: int | None = None
        rating_node = card.select_one("[data-service-review-rating]")
        if rating_node:
            raw_rating = rating_node.get("data-service-review-rating")
            if raw_rating and str(raw_rating).isdigit():
                stars = int(raw_rating)
        if stars is None:
            for image in card.select("img[alt]"):
                stars = _rating_from_alt(image.get("alt", ""))
                if stars is not None:
                    break

        comment = _text(card, (
            "p[data-service-review-text-typography]",
            "[data-service-review-text-typography]",
        ))
        if not (name or date or comment or stars is not None):
            continue
        reviews.append({
            "id": _stable_id(name, date, stars, comment),
            "name": name,
            "date": date,
            "stars": stars,
            "comment": comment,
        })
    return reviews


def _next_page_url(driver: Any) -> str | None:
    from selenium.webdriver.common.by import By

    links = driver.find_elements(
        By.CSS_SELECTOR,
        'a[name="pagination-button-next"][aria-label="Next page"], a[name="pagination-button-next"]',
    )
    if not links:
        return None
    link = links[0]
    if not link.is_enabled() or link.get_attribute("aria-disabled") == "true":
        return None
    href = link.get_attribute("href")
    return href or "__CLICK_NEXT__"


def scrape_reviews(
    url: str,
    *,
    output_path: str | Path | None = None,
    headless: bool = False,
    wait_seconds: int = 20,
) -> "pd.DataFrame":
    """Collect all review pages available from the supplied Trustpilot URL."""
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    destination = Path(output_path) if output_path else Path("data/trustpilot") / "reviews.csv"
    collected: dict[str, dict[str, Any]] = {}
    visited_pages: set[str] = set()

    try:
        driver.get(url)
        while True:
            current_url = driver.current_url
            if current_url in visited_pages:
                raise RuntimeError("صفحه‌بندی Trustpilot به URL تکراری رسید؛ برای جلوگیری از حلقه متوقف شد.")
            visited_pages.add(current_url)

            WebDriverWait(driver, wait_seconds).until(
                lambda d: d.find_elements("css selector", "article[data-service-review-card-paper]")
            )
            page_reviews = parse_review_html(driver.page_source)
            for review in page_reviews:
                collected.setdefault(review["id"], review)

            destination.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(collected.values()).to_csv(destination, index=False, encoding="utf-8-sig")
            LOGGER.info("Trustpilot reviews collected: %d (page %d)", len(collected), len(visited_pages))

            next_url = _next_page_url(driver)
            if next_url is None:
                break
            if next_url == "__CLICK_NEXT__":
                next_button = driver.find_element(
                    "css selector", 'a[name="pagination-button-next"]'
                )
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, wait_seconds).until(lambda d: d.current_url != current_url)
            else:
                if next_url in visited_pages:
                    raise RuntimeError("لینک صفحه بعدی Trustpilot تکراری است؛ استخراج متوقف شد.")
                driver.get(next_url)

        return pd.DataFrame(collected.values())
    finally:
        driver.quit()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Extract reviews from any Trustpilot company URL")
    parser.add_argument("url", nargs="?")
    parser.add_argument("--output")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    url = args.url or input("لینک صفحه نظرات شرکت در Trustpilot را وارد کنید: ").strip()
    frame = scrape_reviews(url, output_path=args.output, headless=args.headless)
    print(f"تعداد نظرات استخراج‌شده: {len(frame)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

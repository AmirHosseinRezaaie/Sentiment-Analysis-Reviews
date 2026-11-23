"""Basalam product-review scraper.

The scraper accepts any supported Basalam product URL and keeps scrolling until
the review list reaches a stable end. It has no configured review-count cap.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def _review_id(name: str, date: str, stars: int | None, text: str) -> str:
    raw = "|".join((name.strip(), date.strip(), str(stars), text.strip()))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _first_text(card: Any, selectors: tuple[str, ...]) -> str:
    for selector in selectors:
        elements = card.find_elements("css selector", selector) if hasattr(card, "find_elements") else []
        if elements:
            element = elements[0]
            value = (element.text or "").strip()
            if value:
                return value
    return ""


def parse_review_cards(section: Any) -> list[dict[str, Any]]:
    """Parse currently rendered review cards; exposed for offline testing."""
    from selenium.webdriver.common.by import By

    cards = []
    for selector in ('div[data-testid*="review"]', "div.eN63l8._9ltxo8"):
        cards = section.find_elements(By.CSS_SELECTOR, selector)
        if cards:
            break

    parsed: list[dict[str, Any]] = []
    for card in cards:
        name = _first_text(card, ("[class*='userName']", ".Rqze5j", "[data-testid*='user']"))
        date = _first_text(card, ("time", ".eN4XZm", "[class*='date']"))
        comment = _first_text(card, ("[data-testid*='comment']", ".nkJy9o", "[class*='comment']", "[class*='reviewText']"))
        try:
            active = card.find_elements(By.CSS_SELECTOR, ".bs-rating__star--active")
            stars: int | None = len(active) if active else None
        except Exception:
            stars = None
        if not (name or date or comment):
            continue
        parsed.append({
            "id": _review_id(name, date, stars, comment),
            "نام کاربر": name,
            "تاریخ": date,
            "امتیاز": stars,
            "متن نظر": comment,
        })
    return parsed


def scrape_reviews(
    url: str,
    *,
    output_path: str | Path | None = None,
    headless: bool = False,
    stable_rounds: int = 5,
    wait_seconds: int = 15,
) -> "pd.DataFrame":
    """Collect all accessible reviews from a Basalam product page.

    ``stable_rounds`` is an end-of-list signal, not a maximum number of
    reviews or scroll operations. Every newly discovered review resets it.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    import pandas as pd

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1024")
    driver = webdriver.Chrome(options=options)
    reviews: dict[str, dict[str, Any]] = {}
    destination = Path(output_path) if output_path else Path("data/basalam") / "reviews.csv"

    try:
        driver.get(url)
        button = WebDriverWait(driver, wait_seconds).until(
            lambda d: d.find_element(By.XPATH, "//button[contains(., 'تجربه خریدها')]")
        )
        driver.execute_script("arguments[0].click();", button)
        section = WebDriverWait(driver, wait_seconds).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "div.bs-modal__content")
        )
        scroll_el = WebDriverWait(driver, wait_seconds).until(
            lambda d: section.find_element(By.CSS_SELECTOR, '[data-testid="virtuoso-scroller"]')
        )

        unchanged_rounds = 0
        previous_position: tuple[int, int] | None = None
        while unchanged_rounds < stable_rounds:
            for review in parse_review_cards(section):
                reviews.setdefault(review["id"], review)

            position = driver.execute_script(
                "return [arguments[0].scrollTop, arguments[0].scrollHeight];", scroll_el
            )
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + Math.max(500, arguments[0].clientHeight * 0.8);",
                scroll_el,
            )
            try:
                WebDriverWait(driver, wait_seconds).until(
                    lambda d: len(parse_review_cards(section)) > 0
                    and d.execute_script(
                        "return [arguments[0].scrollTop, arguments[0].scrollHeight];", scroll_el
                    ) != position
                )
            except Exception:
                # A timeout can mean the end of a virtual list, but it is not
                # enough by itself: require several unchanged observations.
                pass

            for review in parse_review_cards(section):
                reviews.setdefault(review["id"], review)
            current = driver.execute_script(
                "return [arguments[0].scrollTop, arguments[0].scrollHeight];", scroll_el
            )
            if len(reviews) and current == previous_position and current == position:
                unchanged_rounds += 1
            elif current == position and current == previous_position:
                unchanged_rounds += 1
            else:
                unchanged_rounds = 0
            previous_position = tuple(current)

            destination.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(reviews.values()).to_csv(destination, index=False, encoding="utf-8-sig")
            LOGGER.info("Basalam reviews collected: %d", len(reviews))

        return pd.DataFrame(reviews.values())
    finally:
        driver.quit()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Extract reviews from a Basalam product URL")
    parser.add_argument("url", nargs="?")
    parser.add_argument("--output")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    url = args.url or input("لینک محصول باسلام را وارد کنید: ").strip()
    frame = scrape_reviews(url, output_path=args.output, headless=args.headless)
    print(f"تعداد نظرات استخراج‌شده: {len(frame)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Central entry point for collecting reviews from supported websites."""

from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlsplit


class UnsupportedWebsiteError(ValueError):
    """Raised when a URL does not belong to a supported review website."""


@dataclass(frozen=True)
class ScraperTarget:
    name: str
    domains: tuple[str, ...]
    module: str


TARGETS = (
    ScraperTarget("basalam", ("basalam.com",), ".basalam"),
    ScraperTarget("taaghche", ("taaghche.com",), ".taaghche"),
    ScraperTarget("trustpilot", ("trustpilot.com",), ".trustpilot"),
)


def detect_website(url: str) -> str:
    """Return the scraper key for a supported URL, rejecting lookalike hosts."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError("آدرس صفحه خالی است.")

    candidate = url.strip()
    if "://" not in candidate:
        candidate = f"https://{candidate}"
    parsed = urlsplit(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("آدرس واردشده معتبر نیست؛ یک URL با http یا https وارد کنید.")

    host = parsed.hostname.lower().rstrip(".")
    for target in TARGETS:
        if any(host == domain or host.endswith(f".{domain}") for domain in target.domains):
            return target.name
    supported = ", ".join(domain for target in TARGETS for domain in target.domains)
    raise UnsupportedWebsiteError(f"این سایت پشتیبانی نمی‌شود. دامنه‌های پشتیبانی‌شده: {supported}")


def extract_reviews(
    url: str,
    *,
    output_path: str | None = None,
    headless: bool = False,
):
    """Dispatch a URL to its site-specific scraper and return its DataFrame.

    Scrapers continue until the website reports that no further reviews exist;
    there is deliberately no review-count limit in this manager.
    """
    website = detect_website(url)
    target = next(item for item in TARGETS if item.name == website)
    module = importlib.import_module(target.module, package=__package__)
    scraper: Callable = getattr(module, "scrape_reviews")
    return scraper(url, output_path=output_path, headless=headless)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="review-scraper",
        description="Extract reviews from a Basalam, Taaghche, or Trustpilot page.",
    )
    parser.add_argument("url", nargs="?", help="URL of the product, book, or Trustpilot review page")
    parser.add_argument("--output", help="Optional CSV output path")
    parser.add_argument("--headless", action="store_true", help="Run Chrome without a visible window")
    args = parser.parse_args(argv)

    url = args.url or input("لینک صفحه محصول/کتاب/نظرات را وارد کنید: ").strip()
    try:
        website = detect_website(url)
        print(f"سایت شناسایی‌شده: {website}")
        frame = extract_reviews(url, output_path=args.output, headless=args.headless)
    except (ValueError, ImportError, AttributeError, RuntimeError) as exc:
        parser.exit(2, f"خطا در استخراج: {exc}\n")

    print(f"استخراج پایان یافت؛ تعداد نظرات دریافت‌شده: {len(frame)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

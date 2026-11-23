"""Command-line entry point for the sentiment analysis project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from src.sentiment_analysis.scraping.manager import extract_reviews

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    "basalam": ROOT / "notebooks" / "experiments" / "basalam.ipynb",
    "taaghche": ROOT / "notebooks" / "experiments" / "taaghche.ipynb",
    "trustpilot": ROOT / "notebooks" / "experiments" / "trustpilot.ipynb",
}
SCRAPERS = {
    "basalam": ROOT / "src" / "sentiment_analysis" / "scraping" / "basalam.py",
    "taaghche": ROOT / "src" / "sentiment_analysis" / "scraping" / "taaghche.py",
    "trustpilot": ROOT / "src" / "sentiment_analysis" / "scraping" / "trustpilot.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sentiment-project",
        description="Explore the sentiment analysis project workflows.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("overview", help="Show project modules and available workflows.")

    notebook_parser = commands.add_parser("notebook", help="Open an experiment notebook.")
    notebook_parser.add_argument("source", choices=NOTEBOOKS)

    scraper_parser = commands.add_parser("scrape", help="Run an existing website scraper.")
    scraper_parser.add_argument("source", choices=SCRAPERS)

    url_scraper_parser = commands.add_parser(
        "scrape-url",
        help="Detect the website from a URL and run its review scraper.",
    )
    url_scraper_parser.add_argument("url", nargs="?", help="Product, book, or Trustpilot review URL")
    url_scraper_parser.add_argument("--output", help="Optional CSV output path")
    url_scraper_parser.add_argument("--headless", action="store_true", help="Run Chrome without a visible window")

    args = parser.parse_args()

    if args.command == "overview":
        print("Sentiment Analysis Reviews")
        print("1. Web scraping: Basalam, Taaghche, Trustpilot")
        print("2. NLP and preprocessing: notebooks/experiments and src/sentiment_analysis/preprocessing")
        print("3. Machine learning: TF-IDF, Naive Bayes, Logistic Regression, Linear SVM (in notebooks)")
        print("4. Artifacts: data/, models/, figures/, files/, reports/")
        print("\nOpen an experiment: python -m app.main notebook basalam")
        print("Run a scraper:       python -m app.main scrape basalam")
        print("Scrape any URL:      python -m app.main scrape-url")
        return 0

    if args.command == "notebook":
        notebook = NOTEBOOKS[args.source]
        if not notebook.is_file():
            parser.error(f"Notebook not found: {notebook}")
        return subprocess.call([sys.executable, "-m", "jupyter", "lab", str(notebook)], cwd=ROOT)

    if args.command == "scrape-url":
        url = args.url or input("لینک صفحه موردنظر را وارد کنید: ").strip()
        try:
            website_frame = extract_reviews(
                url,
                output_path=args.output,
                headless=args.headless,
            )
        except (ValueError, ImportError, AttributeError, RuntimeError) as exc:
            print(f"خطا در استخراج: {exc}", file=sys.stderr)
            return 2
        print(f"تعداد نظرات استخراج‌شده: {len(website_frame)}")
        return 0

    script = SCRAPERS[args.source]
    if not script.is_file():
        parser.error(f"Scraper not found: {script}")
    return subprocess.call([sys.executable, str(script)], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())

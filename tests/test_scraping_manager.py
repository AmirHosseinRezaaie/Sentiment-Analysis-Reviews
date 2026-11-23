import unittest

from src.sentiment_analysis.scraping.manager import (
    UnsupportedWebsiteError,
    detect_website,
)


class DetectWebsiteTests(unittest.TestCase):
    def test_supported_domains_and_subdomains(self):
        cases = {
            "https://basalam.com/shop/product/123": "basalam",
            "www.basalam.com/shop/product/123": "basalam",
            "https://taaghche.com/book/123/title": "taaghche",
            "https://www.trustpilot.com/review/example.com": "trustpilot",
            "https://uk.trustpilot.com/review/example.com": "trustpilot",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertEqual(detect_website(url), expected)

    def test_rejects_lookalike_domains(self):
        for url in ("https://basalam.com.example.org/item", "https://nottrustpilot.com/review/x"):
            with self.subTest(url=url):
                with self.assertRaises(UnsupportedWebsiteError):
                    detect_website(url)

    def test_rejects_invalid_or_empty_urls(self):
        for url in ("", "   ", "ftp://basalam.com/item", "https:///missing-host"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    detect_website(url)


if __name__ == "__main__":
    unittest.main()

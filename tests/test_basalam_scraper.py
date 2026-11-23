import unittest

from src.sentiment_analysis.scraping.basalam import _review_id


class BasalamReviewIdentityTests(unittest.TestCase):
    def test_review_id_is_stable_across_processes(self):
        first = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        second = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_review_id_changes_when_review_content_changes(self):
        first = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        second = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 4, "نظر نمونه")
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
